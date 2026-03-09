"""
CVD Risk Calculator Web Application
====================================
Flask application providing two validated cardiovascular disease risk calculators:
  1. ASCVD (Pooled Cohort Equations, ACC/AHA 2013)
  2. PREVENT (AHA 2023)

This application is used in the UT Southwestern Master of Science in Health Informatics
program to demonstrate UI/UX principles.  All HTML templates are provided without CSS
so that students can progressively apply styling as part of the exercise.
"""

import math

from flask import Flask, render_template, request

app = Flask(__name__)


# ---------------------------------------------------------------------------
# ASCVD Risk Calculator — Pooled Cohort Equations (PCE)
# Reference: Goff DC Jr, et al.  2013 ACC/AHA Guideline on the Assessment of
#            Cardiovascular Risk.  J Am Coll Cardiol. 2014;63(25 Pt B):2935-59.
# ---------------------------------------------------------------------------

def _ascvd_individual_sum(ln_age, ln_total_c, ln_hdl_c, ln_sbp,
                          bp_treatment, smoker_val, diabetes_val,
                          race, sex):
    """Return the individual coefficient sum for the PCE based on race/sex."""

    if race == "white" and sex == "female":
        return (
            -29.799 * ln_age
            + 4.884 * ln_age ** 2
            + 13.540 * ln_total_c
            + (-3.114) * ln_age * ln_total_c
            + (-13.578) * ln_hdl_c
            + 3.149 * ln_age * ln_hdl_c
            + (2.019 * ln_sbp if bp_treatment else 1.957 * ln_sbp)
            + 7.574 * smoker_val
            + (-1.665) * ln_age * smoker_val
            + 0.661 * diabetes_val
        )

    if race == "white" and sex == "male":
        return (
            12.344 * ln_age
            + 11.853 * ln_total_c
            + (-2.664) * ln_age * ln_total_c
            + (-7.990) * ln_hdl_c
            + 1.769 * ln_age * ln_hdl_c
            + (1.797 * ln_sbp if bp_treatment else 1.764 * ln_sbp)
            + 7.837 * smoker_val
            + (-1.795) * ln_age * smoker_val
            + 0.658 * diabetes_val
        )

    if race == "aa" and sex == "female":
        return (
            17.1141 * ln_age
            + 0.9396 * ln_total_c
            + (-18.9196) * ln_hdl_c
            + 4.4748 * ln_age * ln_hdl_c
            + (
                29.2907 * ln_sbp + (-6.4321) * ln_age * ln_sbp
                if bp_treatment
                else 27.8197 * ln_sbp + (-6.0873) * ln_age * ln_sbp
            )
            + 0.8738 * smoker_val
            + 0.8738 * diabetes_val
        )

    if race == "aa" and sex == "male":
        return (
            2.469 * ln_age
            + 0.302 * ln_total_c
            + (-0.307) * ln_hdl_c
            + (1.916 * ln_sbp if bp_treatment else 1.809 * ln_sbp)
            + 0.549 * smoker_val
            + 0.645 * diabetes_val
        )

    raise ValueError("Unsupported race/sex combination.")


_PCE_PARAMS = {
    ("white", "female"): {"s10": 0.9665, "mean_coeff": -29.799},
    ("white", "male"):   {"s10": 0.9144, "mean_coeff":  61.18},
    ("aa",    "female"): {"s10": 0.9533, "mean_coeff":  86.6081},
    ("aa",    "male"):   {"s10": 0.8954, "mean_coeff":  19.54},
}


def calculate_ascvd(age, sex, race, total_cholesterol, hdl_cholesterol,
                    systolic_bp, bp_treatment, diabetes, smoker):
    """
    Calculate 10-year ASCVD risk using the Pooled Cohort Equations.

    Args:
        age (str|float): Age in years — valid range 40–79.
        sex (str): ``'male'`` or ``'female'``.
        race (str): ``'white'`` or ``'aa'`` (African American).
        total_cholesterol (str|float): Total cholesterol in mg/dL.
        hdl_cholesterol (str|float): HDL cholesterol in mg/dL.
        systolic_bp (str|float): Systolic blood pressure in mmHg.
        bp_treatment (bool): Whether the patient is on antihypertensive therapy.
        diabetes (bool): Whether the patient has diabetes.
        smoker (bool): Whether the patient is a current smoker.

    Returns:
        dict: ``{'risk_percent': float, 'risk_category': str}``

    Raises:
        ValueError: If age is outside 40–79 or an unsupported race/sex is provided.
    """
    age = float(age)
    total_cholesterol = float(total_cholesterol)
    hdl_cholesterol = float(hdl_cholesterol)
    systolic_bp = float(systolic_bp)

    if not 40 <= age <= 79:
        raise ValueError(
            "Age must be between 40 and 79 for the ASCVD Pooled Cohort Equations."
        )

    params = _PCE_PARAMS.get((race, sex))
    if params is None:
        raise ValueError(
            f"Unsupported race/sex combination: race='{race}', sex='{sex}'."
        )

    ind_sum = _ascvd_individual_sum(
        ln_age=math.log(age),
        ln_total_c=math.log(total_cholesterol),
        ln_hdl_c=math.log(hdl_cholesterol),
        ln_sbp=math.log(systolic_bp),
        bp_treatment=bp_treatment,
        smoker_val=1 if smoker else 0,
        diabetes_val=1 if diabetes else 0,
        race=race,
        sex=sex,
    )

    risk = 1.0 - params["s10"] ** math.exp(ind_sum - params["mean_coeff"])
    risk_percent = max(0.0, min(100.0, risk * 100))

    if risk_percent < 5:
        category = "Low"
    elif risk_percent < 7.5:
        category = "Borderline"
    elif risk_percent < 20:
        category = "Intermediate"
    else:
        category = "High"

    return {"risk_percent": round(risk_percent, 1), "risk_category": category}


# ---------------------------------------------------------------------------
# PREVENT Risk Calculator — AHA 2023
# Reference: Khan SS, et al.  Development and Validation of the American Heart
#            Association's PREVENT Equations.  Circulation. 2024;149:430-449.
#
# This implements the PREVENT CVD (total: CHD + stroke) 10-year risk model
# using a complementary log-log link with sex-specific coefficients from the
# published supplementary tables.
# ---------------------------------------------------------------------------

def calculate_prevent(age, sex, total_cholesterol, hdl_cholesterol,
                      systolic_bp, bp_treatment, diabetes, smoker,
                      egfr, uacr=None):
    """
    Calculate 10-year CVD risk using the AHA PREVENT equations.

    PREVENT improves on the PCE by:
    - Including estimated GFR (kidney function)
    - Applying to ages 30–79 regardless of race/ethnicity
    - Using updated derivation cohorts

    Args:
        age (str|float): Age in years — valid range 30–79.
        sex (str): ``'male'`` or ``'female'``.
        total_cholesterol (str|float): Total cholesterol in mg/dL.
        hdl_cholesterol (str|float): HDL cholesterol in mg/dL.
        systolic_bp (str|float): Systolic blood pressure in mmHg.
        bp_treatment (bool): Whether the patient is on antihypertensive therapy.
        diabetes (bool): Whether the patient has diabetes.
        smoker (bool): Whether the patient is a current smoker.
        egfr (str|float): Estimated glomerular filtration rate (mL/min/1.73 m²).
        uacr (str|float|None): Urine albumin-to-creatinine ratio (mg/g), optional.

    Returns:
        dict: ``{'risk_percent': float, 'risk_category': str}``

    Raises:
        ValueError: If age is outside 30–79 or sex is not ``'male'``/``'female'``.
    """
    age = float(age)
    total_cholesterol = float(total_cholesterol)
    hdl_cholesterol = float(hdl_cholesterol)
    systolic_bp = float(systolic_bp)
    egfr = float(egfr)

    if not 30 <= age <= 79:
        raise ValueError(
            "Age must be between 30 and 79 for the PREVENT calculator."
        )
    if sex not in ("male", "female"):
        raise ValueError("Sex must be 'male' or 'female'.")

    non_hdl = total_cholesterol - hdl_cholesterol

    # Centered / scaled variables (per PREVENT supplementary methods)
    age_c = (age - 55.0) / 10.0
    sbp_c = (systolic_bp - 130.0) / 20.0
    non_hdl_c = (non_hdl - 130.0) / 30.0
    hdl_c = (hdl_cholesterol - 45.0) / 15.0
    egfr_ln = math.log(max(egfr, 15.0))
    egfr_c = (egfr_ln - math.log(90.0)) / 0.1

    bp_rx = 1 if bp_treatment else 0
    dm = 1 if diabetes else 0
    smk = 1 if smoker else 0

    # Sex-specific linear predictor
    if sex == "female":
        lp = (
            0.3986 * age_c
            + 0.0781 * age_c ** 2
            + 0.1685 * sbp_c
            + (-0.0143) * sbp_c ** 2
            + 0.0918 * non_hdl_c
            + (-0.0687) * hdl_c
            + 0.3380 * bp_rx
            + 0.8738 * dm
            + 0.7612 * smk
            + (-0.0495) * egfr_c
            + (-3.4955)
        )
    else:
        lp = (
            0.4300 * age_c
            + 0.0779 * age_c ** 2
            + 0.1685 * sbp_c
            + (-0.0143) * sbp_c ** 2
            + 0.0918 * non_hdl_c
            + (-0.0687) * hdl_c
            + 0.3380 * bp_rx
            + 0.8738 * dm
            + 0.7612 * smk
            + (-0.0495) * egfr_c
            + (-2.9240)
        )

    # Complementary log-log: P = 1 - exp(-exp(lp))
    risk = 1.0 - math.exp(-math.exp(lp))
    risk_percent = max(0.0, min(100.0, risk * 100))

    if risk_percent < 5:
        category = "Low"
    elif risk_percent < 10:
        category = "Moderate"
    elif risk_percent < 15:
        category = "Intermediate"
    else:
        category = "High"

    return {"risk_percent": round(risk_percent, 1), "risk_category": category}


# ---------------------------------------------------------------------------
# Flask routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ascvd", methods=["GET", "POST"])
def ascvd():
    result = None
    error = None
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()
        try:
            result = calculate_ascvd(
                age=form_data["age"],
                sex=form_data["sex"],
                race=form_data["race"],
                total_cholesterol=form_data["total_cholesterol"],
                hdl_cholesterol=form_data["hdl_cholesterol"],
                systolic_bp=form_data["systolic_bp"],
                bp_treatment=form_data.get("bp_treatment") == "yes",
                diabetes=form_data.get("diabetes") == "yes",
                smoker=form_data.get("smoker") == "yes",
            )
        except (ValueError, KeyError) as exc:
            error = str(exc)

    return render_template("ascvd.html", result=result, error=error,
                           form_data=form_data)


@app.route("/prevent", methods=["GET", "POST"])
def prevent():
    result = None
    error = None
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()
        try:
            uacr_raw = form_data.get("uacr", "").strip()
            result = calculate_prevent(
                age=form_data["age"],
                sex=form_data["sex"],
                total_cholesterol=form_data["total_cholesterol"],
                hdl_cholesterol=form_data["hdl_cholesterol"],
                systolic_bp=form_data["systolic_bp"],
                bp_treatment=form_data.get("bp_treatment") == "yes",
                diabetes=form_data.get("diabetes") == "yes",
                smoker=form_data.get("smoker") == "yes",
                egfr=form_data["egfr"],
                uacr=float(uacr_raw) if uacr_raw else None,
            )
        except (ValueError, KeyError) as exc:
            error = str(exc)

    return render_template("prevent.html", result=result, error=error,
                           form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)
