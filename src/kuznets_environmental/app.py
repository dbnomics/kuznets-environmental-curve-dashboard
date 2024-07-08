import streamlit as st
import importlib
from data_loader import load_data_depletion, merge_country_depletion, load_data_greenhouse, merge_country_greenhouse
from charts_creator import plot_kuznets_curve_depletion, plot_kutznet_curve_greenhouse, plot_greenhouse

from streamlit_option_menu import option_menu

def main():
    package_dir = importlib.resources.files("kuznets_environmental")
    st.set_page_config(
        page_title="DBnomics Kuznets Environmental Curve",
        page_icon=str(package_dir / "images/favicon.png"),
    )
    st.image(str(package_dir / "images/dbnomics.svg"), width=300)
    st.title(":blue[Kuznets Environmental Curve]")

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("styles.css")
    st.markdown(
        """
        <style>
        hr {
            height: 1px;
            border: none;
            color: #333;
            background-color: #333;
            margin-top: 3px;
            margin-bottom: 3px;
        }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Explanations", "Natural Resource Depletion",
                     "Greenhouse Gas Emission","Greenhouse Gas Emission for all countries" ,"Sources", "DBnomics"],
            icons=["book", "bar-chart","bar-chart","bar-chart", "paperclip", "search"],
            menu_icon=":",
            default_index=0,
        )

    if selected == "Explanations":
        st.header("What is the Kuznets Environmental Curve?")
        st.write(
            "\n"
            "**Simon Kuznets** (1901-1985) was an American economist who received the Nobel Prize in Economics in 1971 for his work on economic growth and development.\n"
            "\n"
            "Kuznets' main work focuses on the cycles of growth. He conducted empirical research on long-term series.\n"
            "\n"
            "In this presentation, we are interested in Kuznets' hypotheses concerning the environment.\n"
            "Kuznets argues for an inverse relationship, starting from a certain stage of development, between pollution and per capita income.\n"
            "Economic growth, at its beginning, leads to an increase in pollution: infrastructure, production, consumption, exports, and imports.\n"
            "From a certain level of wealth, economies pay more attention to the environment.\n"
            "Thus, economic growth beyond a certain point would be beneficial for the environment.\n"
            "\n"
            " There is no consensus on this relationship between the two indicators.\n"
            "Moreover, empirical data tend to show the opposite: the more economic growth there is, the more economies tend to pollute.\n"
            "Policies and measures to protect the environment are necessary: economic growth alone does not limit the impacts of economic growth on the environment.\n"
            "\n"
        )

    if selected == "Natural Resource Depletion":
        df_gdp, df_depl = load_data_depletion()
        merged_dfs = merge_country_depletion((df_gdp, df_depl))

        country = st.selectbox("Select a country for Natural Resource Depletion", list(merged_dfs.keys()))

        if country:
            fig = plot_kuznets_curve_depletion(merged_dfs[country], country)
            st.plotly_chart(fig)
    
    if selected == "Greenhouse Gas Emission":
        df_gdp, df_green = load_data_greenhouse()
        merged_newdfs = merge_country_greenhouse((df_gdp, df_green))

        country = st.selectbox("Select a country for Greenhouse Gas Emission", list(merged_newdfs.keys()))

        if country:
            fig = plot_kutznet_curve_greenhouse(merged_newdfs[country], country)
            st.plotly_chart(fig)

    if selected == "Greenhouse Gas Emission for all countries":
        df_gdp, df_green = load_data_greenhouse()
        merged_newdfs = merge_country_greenhouse((df_gdp, df_green))

        fig = plot_greenhouse(merged_newdfs)
        st.plotly_chart(fig)

    if selected == "Sources": 
        st.write(
            "\n"
            "GDP per capita : [link](https://db.nomics.world/WB/WDI?dimensions=%7B\"indicator\"%3A%5B\"NY.GDP.PCAP.KD\"%5D%7D&tab=list)\n"
            "\n"
            "Natural Resource depletion : [link](https://db.nomics.world/WB/WDI?dimensions=%7B\"indicator\"%3A%5B\"NY.ADJ.DRES.GN.ZS\"%5D%7D&tab=list)\n"
            "\n"
            "Greenhouse gas emission : [link](https://db.nomics.world/WB/WDI?dimensions=%7B\"indicator\"%3A%5B\"EN.ATM.GHGT.KT.CE\"%5D%7D&tab=list)"
        )

    if selected == "DBnomics":
        st.write("Visit DBnomics by clicking [here](https://db.nomics.world)")
if __name__ == "__main__":
    main()
