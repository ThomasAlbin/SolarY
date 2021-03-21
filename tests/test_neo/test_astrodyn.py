"""Testing suite for SolarY/neo/astrodyn.py"""

# Import SolarY
import SolarY


def test_neo_class():
    """
    Testing the neo classification function

    Returns
    -------
    None.

    """

    # Based on values from
    # 1221 Amor
    # 1862 Apollo
    # 2062 Aten
    # 163693 Atira
    neo_sample = {
        "Amor": {"sem_maj_axis_au": 1.9198, "peri_helio_au": 1.0856, "ap_helio_au": 2.7540},
        "Apollo": {"sem_maj_axis_au": 1.4702, "peri_helio_au": 0.64699, "ap_helio_au": 2.2935},
        "Aten": {"sem_maj_axis_au": 0.967, "peri_helio_au": 0.79, "ap_helio_au": 1.143},
        "Atira": {"sem_maj_axis_au": 0.7411, "peri_helio_au": 0.5024, "ap_helio_au": 0.9798},
    }

    # Iterate trough all NEO class expectations
    for _neo_class_exp in neo_sample:

        # Determine the NEO class
        neo_class_res = SolarY.neo.astrodyn.neo_class(
            sem_maj_axis_au=neo_sample[_neo_class_exp]["sem_maj_axis_au"],
            peri_helio_au=neo_sample[_neo_class_exp]["peri_helio_au"],
            ap_helio_au=neo_sample[_neo_class_exp]["ap_helio_au"],
        )

        # Check the classification with the expectation
        assert neo_class_res == _neo_class_exp
