import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache
def load_file():
    #source repository https://github.com/owid/co2-data
    df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
    df = df[df["year"].notnull()]
    df["year"] == df["year"].astype("int")
    df_column_meta = pd.read_csv("column_metadata.csv")
    return df, df_column_meta

@st.cache
def convert_df(df, require_index = False):
     return df.to_csv(index=require_index).encode('utf-8-sig')



def main():
    st.header("温室効果ガス排出量ダッシュボード")

    #データの読み込み
    df ,df_column_meta = load_file()

    #パラメタの選択
    gas_types = ["二酸化炭素","全ての温室効果ガス", "メタン","亜酸化窒素"]
    gas_type = st.selectbox("ガスの種類を選択",gas_types)

    df_column_meta = df_column_meta[df_column_meta["gas_type"] == gas_type]
    accounting_type = st.selectbox("算出手法を選択", df_column_meta["accounting_type"].unique())
    df_column_meta = df_column_meta[df_column_meta["accounting_type"] == accounting_type]
    if (gas_type=="二酸化炭素")& (accounting_type == "生産ベース"):
        fuel_type = st.selectbox("燃料タイプを選択", df_column_meta["fuel_type"].unique())
        df_column_meta = df_column_meta[df_column_meta["fuel_type"] == fuel_type]
    else:
        fuel_type = None
    count_type = st.selectbox("単位を選択",  df_column_meta["count_type"].unique())
    df_column_meta = df_column_meta[df_column_meta["count_type"] == count_type]

    if  (gas_type=="二酸化炭素")&(accounting_type == "生産ベース")&(fuel_type == "その他")&(count_type == "実数"):
        is_relative = st.checkbox("世界全体に対する相対値で表示", value=True, disabled = True)
    else:
        is_relative = st.checkbox("世界全体に対する相対値で表示", value=False, disabled=((gas_type!="二酸化炭素")|(accounting_type != "生産ベース"))&(count_type != "貿易に伴う排出量"))
    df_column_meta = df_column_meta[df_column_meta["relative_to_world"] == is_relative]
    assert df_column_meta.shape[0] == 1

    column_name = df_column_meta.iloc[0]["column"]
    unit_name = df_column_meta.iloc[0]["unit"]
    title_name = gas_type
    if accounting_type:
        title_name += f"_{accounting_type}"
    if fuel_type:
        title_name += f"_{fuel_type}"
    if count_type:
        title_name += f"_{count_type}"
    if is_relative:
        title_name += "_世界全体に対する相対値"
    title_name += f"({unit_name})"
    tab1, tab2, tab3 = st.tabs(["CHART","MAP","TABLE"])

    #折れ線グラフ
    with tab1:
        plot_countries = st.multiselect("国と地域を選択",df["country"].unique(),
        ["World","Japan","United States","China","Russia","France"])
        is_logplot = st.checkbox("対数表示", value=False, disabled=(count_type != "実数"))
        df_plot = df[df[column_name].notnull() & df["country"].isin(plot_countries)]
        fig = px.line(df_plot, x="year", y=column_name, color="country",
                    title=title_name, template="simple_white",
                    log_y=is_logplot)
        fig.update_xaxes(title="年")
        fig.update_yaxes(title="", tickformat = "3.0f", rangemode = "tozero")
        st.plotly_chart(fig, use_container_width=True)

        csv = convert_df(df_plot[["year","iso_code","country",column_name]])

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{title_name}.csv',
            mime='text/csv',
        )
    #コロプレスマップ
    with tab2:
        df_plot = df[df["iso_code"].notnull() & df[column_name].notnull()]
        year_plot = st.slider("年を選択", min_value=df_plot["year"].min(), max_value=df_plot["year"].max(), value=df_plot["year"].max(), step=1)
        df_plot = df_plot[df_plot["year"] == year_plot]
        fig = px.choropleth(df_plot,
                    locations = "iso_code", color = column_name, hover_data = ["country",column_name], color_continuous_scale="Viridis",
                    title=title_name)
        fig.update_coloraxes(colorbar_tickformat="3f", colorbar_title= unit_name)
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
        print(df_plot.columns)
        csv = convert_df(df_plot[["year","iso_code","country",column_name]])
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{title_name}_map.csv',
            mime='text/csv',
        )
    #テーブル
    with tab3:
        df_plot = df[df[column_name].notnull()]
        st.subheader(title_name)
        year_start = st.slider("比較する年を選択(古)", min_value=df_plot["year"].min(), max_value=df_plot["year"].max()-1, value=df_plot["year"].max()-10, step=1)
        year_end = st.slider("比較する年を選択(新)", min_value=year_start+1, max_value=df_plot["year"].max(), value=df_plot["year"].max(), step=1)
        df_plot = df[(df["year"].isin([year_start,year_end]))].pivot_table(column_name,"country","year")
        df_plot[f"{year_start}年と{year_end}年の差({unit_name})"] = df_plot[year_end] -  df_plot[year_start]
        df_plot[f"{year_start}年と{year_end}年の変化率(%)"] = 100*(df_plot[year_end].div(df_plot[year_start]) - 1.)
        csv = convert_df(df_plot, require_index=True)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{title_name}_{year_start}_vs_{year_end}.csv',
            mime='text/csv',
        )
        st.table(df_plot)

if __name__ == "__main__":
    main()