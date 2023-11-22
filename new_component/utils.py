import streamlit as st



def get_attribute(obj: object, attr: str) -> any:
    if hasattr(obj, "__getattribute__"):
        return obj.__getattribute__(attr)
    raise AttributeError("the object does not have  __getattribute__")


def has_numbers(listString):
    for inputString in listString :
        if not any(char.isdigit() for char in str(inputString)):
            return False
    return True


def portfolio_link():
    return st.markdown(
        """
            <p style="text-align: center;">
                <a href="https://mokhles-abdelmonem-portfolio.streamlit.app">
                    Visit My Portfolio
                </a>
            </p>
        """,
        unsafe_allow_html=True)


measures_methodes ={
    "SUM":"sum",
    "AVRAGE":"mean",
    "MEDIAN":"median",
    "COUNT":"count",
    "COUNT (DISTINCT)":"count",
    "MINIMUM":"min",
    "MAXIMUM":"max",
    "STANDARD DEVIATION":"std",
    "STANDARD DEVIATION (POPULATION)":"std",
    "VARIANCE":"var",
    "VARIANCE (POPULATION)":"var",
}
