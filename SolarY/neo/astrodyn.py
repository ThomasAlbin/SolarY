"""NEO related astro-dynamical functions and classes."""


def neo_class(sem_maj_axis_au: float,
              peri_helio_au: float,
              ap_helio_au: float) -> str:
    """Classify the NEO based on the orbital parameters.

    Depending on the semi-major axis, perihelion and / or aphelion a NEO can be classified as an
    Amor, Apollo, Aten or Atira.

    Parameters
    ----------
    sem_maj_axis_au : float
        Semi-major axis of the NEO. Given in AU
    peri_helio_au : float
        Perihelion of the NEO. Given in AU
    ap_helio_au : float
        Aphelion of the NEO. Given in AU

    Returns
    -------
    neo_type : str
        NEO class / type.

    References
    ----------
    -1- Link to the NEO classifiction schema: https://cneos.jpl.nasa.gov/about/neo_groups.html
    """
    # Determine the NEO class in an extensive if-else statement
    if (sem_maj_axis_au > 1.0) & (1.017 < peri_helio_au < 1.3):
        neo_type = 'Amor'

    elif (sem_maj_axis_au > 1.0) & (peri_helio_au < 1.017):
        neo_type = 'Apollo'

    elif (sem_maj_axis_au < 1.0) & (ap_helio_au > 0.983):
        neo_type = 'Aten'

    elif (sem_maj_axis_au < 1.0) & (ap_helio_au < 0.983):
        neo_type = 'Atira'

    else:
        neo_type = 'Other'

    return neo_type
