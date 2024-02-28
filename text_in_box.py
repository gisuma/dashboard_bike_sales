import streamlit as st
from babel.numbers import format_currency


def text_boxs(label_box='Label',value_box='Value',Colour_box=(0,204,102),label_font_size=20,value_font_size=50,currency_format=False):
    wch_colour_box = Colour_box
    wch_colour_font = (0,0,0)
    fontsize = label_font_size
    fontsize2 = value_font_size
    valign = "Center"
    sline = label_box
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    if currency_format:
        i = format_currency(round(value_box,2), 'USD', locale='en_US')
    else:
        i = round(value_box,2)

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;
                        text-align:center;
                        vertical-align: middle;
                        border-style: solid;
                        border-color: black;'>
                        {sline}
                        </style><BR><BR><span style='font-size: {fontsize2}px;'>{i}</span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)