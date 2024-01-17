import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go

import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

energy_data = pd.read_csv('net_gen_all_fuels_nj.csv')
energy_data = energy_data.drop(['Month'], axis = 1) 
energy_data = energy_data.drop(['bymonth'], axis = 1) 


css_directory = os.getcwd()
static_css_route = '/assets/'
color_1 = "#117177"

#df = pd.read_csv('data/proscons.csv')
colors = {"background": "#0B4C5F", "background_div": "white"}

def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        
        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ]
    )


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Power Controller Review"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Img(src='https://cdn.arstechnica.net/wp-content/uploads/2014/06/2449377038_3d803e6db0_z.jpg',height="100%")
                ],
            ),
        ],
    )

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="overview_tab",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="overview-tab",
                        label="Overview",
                        value="overview_tab",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div(className='overview-tab', children=[
                                html.H4(
                                    className='what-is',
                                    children='Why use a power controller?'
                                ),
                                html.H6(
                                    """
                                    The MCP1500 employs power isolation. Such isolation helps to reject external noise sources such as motors, lights, and dimmers commonly found in the home environment. 
                                    Torus power products provide noise filtering at a range from approximately 2000Hz to over 1MHz – other regular transformer based 
                                    products do not start operating until nearly 10,000 Hz.
                                    """
                                ),
                                html.H6(
                                    """
                                    It can be proven that up to a third of a high-resolution (low-level) audio signal can be lost, masked, or highly distorted by the vast levels of noise riding along the AC power lines that feed our components. 
                                    This noise couples with the signal circuitry as current noise and through AC ground, permanently distorting and/or masking the source signal. Our systems’ sensitive components need better alternating current.
                                    """
                                ),
                                dcc.Graph(
                                    id="control-chart-container",
                                                            figure={
                                                                
                                                                "data": [
                                                                    go.Scatter(
                                                                        x=energy_data[
                                                                            "year"
                                                                        ],
                                                                        y=energy_data[
                                                                            "byyear"
                                                                        ],
                                                                        hoverinfo="y+name",
                                                                        line={
                                                                            "color": color_1,
                                                                            "width": 1.5,
                                                                        },
                                                                        name="MW hours",
                                                                    ),
                                                                ],
                                                                "layout": go.Layout(
                                                                    height=500,
                                                                    width = 1120,
                                                                    title = "Net Energy Data in NJ", 
                                                                    xaxis={
                                                                        "range": [
                                                                            2000,
                                                                            2020,
                                                                        ],
                                                                        "showgrid": False,
                                                                        "showticklabels": True,
                                                                        "tickangle": -90,
                                                                        "tickcolor": "#b0b1b2",
                                                                        "tickfont": {
                                                                            "family": "Arial",
                                                                            "size": 12,
                                                                        },
                                                                        "tickmode": "linear",
                                                                        "title": 'Year',
                                                                         "titlefont": {
                                                                            "size": 15,
                                                                            "color": "black",
                                                                        },
                                                                        "ticks": "",
                                                                        "type": "linear",
                                                                        "zeroline": True,
                                                                        "zerolinecolor": "#FFFFFF",
                                                                    },
                                                                    yaxis={
                                                                        "autorange": False,
                                                                         "range": [
                                                                            0,
                                                                            7000,
                                                                        ],
                                                                        "linecolor": "#b0b1b2",
                                                                        "nticks": 9,
                                                                        "title": 'Net Energy Generation All Fuels NJ (thousand megawatthours)',
                                                                        "titlefont": {
                                                                            "size": 15,
                                                                            "color": "black"
                                                                        },
                                                                        "showgrid": False,
                                                                        "showline": True,
                                                                        "tickcolor": "#b0b1b2",
                                                                        "tickfont": {
                                                                            "family": "Arial",
                                                                            "size": 12,
                                                                        },
                                                                        "ticks": "outside",
                                                                        "type": "linear",
                                                                        "zerolinecolor": "#b0b1b2",
                                                                    },
                                                                    hovermode="closest",
                                                                    legend={
                                                                        "x": 0.5,
                                                                        "y": -0.4,
                                                                        "font": {
                                                                            "size": 9
                                                                        },
                                                                        "orientation": "h",
                                                                        "xanchor": "center",
                                                                        "yanchor": "bottom",
                                                                    },
                                                                    
                                                                ),
                                                            }
                                                        ),
                             html.H5(
                                    children = 'User Feedback:'
                                ),
                                html.P(
                                    """
                                    "Mouse
                                    10-29-2017, 01:48 AM
                                    I'm thinking of getting one too, but I'm reading about it's design faults too which makes me apprehensive. Mostly it just filters noise in the power from the wall, it doesn't reduce noise coming from other component connected to the same power conditioner. I have a free Panamax. It's one of the better ones with a removable cable, but probably not comparable to the Mc. 

                                    I'm thinking of getting one too, but I'm reading about it's design faults too which makes me apprehensive. Mostly it just filters noise in the power from the wall, it doesn't reduce noise coming from other component connected to the same power conditioner. I have a free Panamax. It's one of the better ones with a removable cable, but probably not comparable to the Mc. 

                                    But I want my system to look pretty, so here I am talking about it instead of buying it. 
                                    I was thinking of starting a new thread on this when I saw this one pop up recently."
                                    """
                                ),
                                html.P(
                                    """
                                    "cleeds
                                    10-29-2017, 09:28 AM
                                        There are so many variables in the quality of AC power between locations that it's very difficult to predict how well something like an MPC-1500 will work for you. Sometimes AC quality can change - for better or worse - even in the same location. 

                                        For example, I had terrible AC power when I first bought my house, and was particularly plagued with low voltage. But gradual improvements by the electric utility have helped over time. The two things that made the biggest difference were substation upgrades and a change to our street's circuit when a neighbor installed solar power. Reliability improvements ordered by the state after Hurricane Sandy have also helped my house have much better quality AC than before.

                                        I used to use an API Ultra 116 balanced power unit plugged into an API Ultra 2-20 for all of my line level components and it was terrific. That was plugged into a dedicated derated 20A line. But when I upgraded by preamp and phono stage a while back, the current demand of the new gear exceeded what the API allowed on its individual outlets. So I replaced the Ultra 116 with an MPC-1500 and there was no loss in performance at all - even though I have both analog and digital gear plugged into it. (I kept the Ultra 2-20 and the MPC-1500 itself is plugged into it. Don't ask me why I did that. I don't know if it helps or not.) 

                                        If you're tempted by the MPC-1500, I suggest you ask your dealer to loan you a unit so that you can evaluate it for yourself. Perhaps I would not have been happy with mine back when my AC power was so poor. There's no way to know. But I have zero complaints with it now. And the convenience of the remote triggers is also nice.

                                        While we're on the subject, I also use a Tice Power Block and Titan pair on each of my amplifiers. They are very, very effective and I have no plan to upgrade them. The MPC-1500 is for use only on line level gear."
                                     """
                                ),
                            ])
                        ),
                    dcc.Tab(
                        id="mcp1500-tab",
                        label="McIntosh MCP1500",
                        value="mcp1500_tab",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div(className='mcp1500-tab', children=[
                                html.Img(className = "mcp1500_img", src='https://www.mcintoshlabs.com/-/media/Images/mcintoshlabs/Products/ProductImages/MPC1500/MPC1500-Angle.ashx',height="100%"),
                                html.H4(
                                    """
                                    Power Isolation
                                    """
                                ),
                                html.H6(
                                    """
                                    This unit is a toroidal isolation transformer. The system acts as a low pass filter to remove unwanted noise in the circuit. There is different insulation between the primary and secondary winding which blocks electrical interference and therefore noise.
                                    """
                                ),
                                html.P(
                                    """
                                    The MCP1500 is microprocessor controlled, which is superior because they monitor current and use relays to physically and completely disconnect the circuit.
                                    This is a quick-acting surge suppression module.
                                    The system releases excess voltage from surge to a neutral instead of a grounded wire to ensure that it will not find its way back into audio components.
                                    """,
                                    className = "mcp1500marg"
                                ),
                                html.H5(
                                    """
                                    What are the benefits of a toroidal isolation transformer?
                                    """
                                ),
                                html.P(
                                    """
                                   They do not radiate much of a magnetic field, unlike other units, this is an advantage. 
                                   The outside layers of winding around the core of wire are vulnerable to damage.
                                    The transformer laminated metal core can become saturated if too much DC offset is at the input power.
                                    This system is completely isolated from ground, which can be bad for energy build up, but it does not contaminate ground power with extra voltage.
                                    Regulating the voltage reduces the stress on equipment.

                                    """,
                                    className = "mcp1500-margin"
                                ),
                        ],
                        ),
                    ),
                      dcc.Tab(
                        id="mcp500-tab",
                        label="McIntosh MCP500",
                        value="mcp500_tab",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div(className='mcp500-tab', children=[
                                html.Img(className = "mcp500_img", src='https://www.mcintoshlabs.com/-/media/Images/mcintoshlabs/Products/ProductImages/MPC500/MPC500-Angle-left.ashx',height="100%"),
                                html.H4(
                                    """
                                    Power Conditioner
                                    """
                                ),
                                html.H6(
                                    """
                                    “Much safer than traditional self-sacrificing MOV’s”      
                                    "The MCP500 is more affordable to take back business from third party manufacturers"
                                    """
                                ),
                                html.P(
                                    """
                                    This is a full mode AC power line surge protection unit. It has low voltage secondary surge protection.
                                    Its components are thermally protected metal-oxide varistors (TPMOV’s), which are safer than traditional MOV’s. They are line to neutral, line to ground, and neutral to ground.
                                    """,
                                    className = "mcp500margin"
                                ),
                                html.H5(
                                    """
                                    How do the components of this unit work, and what are they?
                                    """
                                ),
                                html.P(
                                    """
                                    It has gas discharge tubes, positive temperature coefficient thermistors and transient voltage suppression.
                                    """,
                                    className = "mcp500p"
                                ),
                                html.P(
                                    """
                                    PTC thermistors are resistors with a positive temperature coefficient, which means that the resistance increases with increasing temperature.In the event of an over-current (or short-circuit) situation, the PTC thermistor increases in temperature and reaches the transition temperature, so then resistance is applied by the thermistor until the over-current situation is solved and it cools down again.
                                    """
                                ),
                                 html.P(
                                    """
                                    A specialized type of gas-filled tube called a Gas Discharge Tube (GDT) is fabricated for use as surge protectors, to limit voltage surges in electrical and electronic circuits. A Gas Discharge Tube or GDT can be used as a standalone component or combined with other components to make a multistage protection circuit – the gas tube acts as the high energy handling component. GDT’s are typically deployed in the protection of communication and data line DC voltage applications because of its very low capacitance. However, they provide very attractive benefits on the AC power line including no leakage current, high energy handling and better end of life characteristics.
                                    """
                                ),
                                 html.P(
                                    """
                                    Transient voltage suppressor diodes are very popular devices used to instantaneously clamp transient voltages (e.g., ESD events) to safe levels before they can damage a circuit. Although standard diodes and Zener diodes can both be used for transient protection, they are actually designed for rectification and voltage regulation, and, therefore, are not as reliable or robust as transient voltage suppressor diodes. They are low energy handling.
                                    """
                                ),
                        ],
                        ),
                    ),
                    dcc.Tab(
                        id="niag7000-tab",
                        label="Niagara 7000",
                        value="niag7000_tab",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div(className='niag7000_tab', children=[
                                html.Img(className = "niag7000_img", src='https://www.audioquest.com/content/aq/img/Niagara-7000-internal.jpg',height="100%"),
                                html.H4(
                                    """
                                    Niagara 7000 Low-Z Power Noise-Dissipation System
                                    """
                                ),
                                html.H6(
                                    """
                                    The Niagara 7000 affords extremely low system noise and provides superior current delivery across a very wide range of frequencies.
                                    """,
                                    className = "niag7000marg"
                                ),
                                html.P(
                                    """
                                    In the Niagara 7000, you’ll find optimized radio-frequency lead directionality, run-in capacitor forming technologies developed by 
                                    Jet Propulsion Laboratories and NASA, and AC inlet and outlet contacts with heavy silver plating over extreme-purity copper assuring the tightest grip possible.
                                    """,
                                    className = "niag17000marg"
                                ),
                                html.H5(
                                    """
                                    How does this unit work? What are the components and capabilities?
                                    """
                                ),
                                html.P(
                                    """
                                    It has High Current - AC Outlets, Ultra-Linear Dierential / Common-Mode Filter – Non-Sacrificial Surge Suppressor
                                    and transient voltage suppression, Transient Power Correction, Ground Noise-Dissipation System, Two Discrete Symmetrical AC Power Isolation Transformers, and Dielectric-Bias Transformer Supply.
                                    """,
                                    className = "mcp500p"
                                ),
                                html.P(
                                    """
                                    High Current - AC Outlets: 6 isolated AC power outlet banks with 16 amp RMS average (@220-240VAC 50/60Hz) current capacity (high current), and 2 source outlet banks of 4 outlets each, with 3 amps total capacity per group. These outlets utilize high spring-strength beryllium copper base metal with heavy silver-plated contacts. This assures far lower loss and distortion, while providing a superior means of draining radio frequency noise.
                                    """
                                ),
                                 html.P(
                                    """
                                    Ultra-Linear Dierential / Common-Mode Filter – Non-Sacrificial Surge Suppressor
                                    and transient voltage suppression: Over a third of low-level audio/video resolution can be masked or lost to induced radio frequency and AC noise. The Niagara filters are optimized for real-world impedance and cover an unprecedented range of over 21 octaves. Non-sacrificial surge protection and auto over-voltage shutdown mean that your components will be protected, AND the Niagara will also protect itself. Set and forget level protection.
                                    """
                                ),
                                 html.P(
                                    """
                                    Transient Power Correction: From nimble, efficient Class-D to mammoth Class-A mono block power amplifiers, average (RMS) current draw can be modest (2 to 7 amps). However, wide dynamic range audio content can create very fast transient current demands…. as much as ten times that average. Our correction circuit bolsters and stabilizes the power supply of any power amplifier by providing a buffer and an instant current reservoir of up to 80 amps peak (20mS).
                                    """
                                ),
                                 html.P(
                                    """
                                    Ground Noise-Dissipation System: signals. This is critical as the AC ground is directly connected to component circuit ground. Employed in concert withour Ultra-Linear filters and direction oriented, grain-controlled AudioQuest AC cables, this ensures the highest resolution and lowest distortion performance from your system components.
                                    """
                                ),
                                 html.P(
                                    """
                                    Two Discrete Symmetrical AC Power Isolation Transformers: These massive transformers provide 100% isolation from the middle four AC source outlets, from the middle four source AC outlets and the high current AC outlets. Additionally, symmetrical induced noise (common-mode) is reduced to the lowest level possible, over the widest range of frequencies possible.
                                    """
                                ),
                                 html.P(
                                    """
                                    Dielectric-Bias Transformer Supply: By electrostatically charging the insulation materials in the isolation transformers, the efficiency and linearity (consistency) of the filter is greatly improved. This technology provides greater clarity for connected system components by greatly reducing noise masking and distortion. This is particularly critical at the highest frequencies where ordinary isolation transformers will fail.
                                    """
                                ),
                        ],
                        ),
                    ),
                    dcc.Tab(
                        id="IT-REF-20I-tab",
                        label="Furman IT-REF 20I",
                        value="IT-REF-20I_tab",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div(className='IT-REF-20I_tab', children=[
                                html.Img(className = "IT-REF-20I_img", src='https://www.furmanpower.com/sites/default/files/styles/product_featured/public/_/products/IT-REF-20I_main-01.jpg?itok=tc5vCAPI',height="80%"),
                                html.H4(
                                    """
                                    Power Conditioner - Non Sacrificial
                                    """
                                ),
                                html.H6(
                                    """
                                    Clean and condition your AC power while meeting the extreme AC power demands of amplifiers with Power Factor Technology.
                                    """,
                                    className = "mcp500marg"
                                ),
                                html.P(
                                    """
                                    With the IT-REFERENCE 20i's exclusive Discrete Symmetrical Power, video screens, projectors, CD-DVD players, pre-amplifiers, and scalers are fed linearly-filtered ultra-low-noise symmetrical power. 
                                    """,
                                    className = "mcp500marg"
                                ),
                                html.H5(
                                    """
                                    How does this unit work? What are the components and capabilities?
                                    """
                                ),
                                html.P(
                                    """
                                        This system has: Extreme Voltage Shutdown, Series Multi-Stage Protection, and Non-sacrificial protection with zero ground contamination capabilities.
                                    """,
                                    className = "mcp500p"
                                ),
                                html.P(
                                    """
                                    The IT-Reference 20i's Discrete Symmetrical Power features total isolation between the filtered-high current outlets, and the isolated symmetrical power AC outlet banks. This positively breaks noiseinducing ground loops, hum bars, and power supply backwash between critical interconnected equipment, all without compromising electrical safety. Furman's newly refined Dual-Screen Transformers yield the widest bandwidth of noise-reduction possible. This enables the IT-REFERENCE 20i to uncover unprecedented levels of video and audio detail, while insuring that plasmas, LCD screens, or video projectors are free of AC ground contamination from an audio processor or power amplifiers.
                                    So, it has some power isolation invovled in its system. The IT-REFERENCE 20i also employs our unique Power Factor Technology circuit. For the first time, low-level analog, digital, and video components are not modulated or distorted via the power amplifier's extreme AC current demands. Further, the power amplifier sees a highly filtered, extremely low-impedance supply of AC power. The IT-REFERENCE 20i, in fact, has in excess of 9 Amps of continuous current reserve (over 80 amps peak charge) for the most extreme peak power demands. This technology enables power amplifiers and powered subwoofers to work at peak efficiency and reach levels of performance previously unattainable.
                                    """
                                ),
                        ],
                        ),
                    ),
                      dcc.Tab(
                        id="comparison-tab",
                        label="Comparison",
                        value="comparison_tab",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div(className='comparison-tab', children=[
                                html.Img(className = "both-one", src='https://www.mcintoshlabs.com/-/media/Images/mcintoshlabs/Products/ProductImages/MPC500/MPC500-Angle-left.ashx',height="100%"),
                                html.Img(className = "both-two", src='https://www.mcintoshlabs.com/-/media/Images/mcintoshlabs/Products/ProductImages/MPC1500/MPC1500-Angle.ashx',height="100%"),
                                html.H2(
                                    """
                                    McIntosh Units

                                    """,
                                    className = "mcintosh"
                                ),
                                html.H5(
                                    """
                                    Both units have B/F receptacles. The load regulation of the MPC1500 is +/- 2.5% but the load regulation of the MCP500 is N/A.

                                    """,
                                    className = "both-three"
                                ),
                                html.H5(
                                    """
                                    Load regulation is the ability of the power supply to maintain its specified output voltage given changes in the load. This does not mean the tolerance applies when there are sudden changes in load, it means over the permissible load range the regulation can change by this amount.

                                    Take an unregulated 12V output DCDC specified with:
                                    Line regulation: 1.2%
                                    Load regulation: 7.5%
                                    So for changes in line input voltage the output voltage can vary by +-144mV and for changes in line load output voltage can vary by +-900mV. So the actual output voltage will be in the range of 10.97V to 13.04V 

                                    """,
                                    className = "both-four"
                                ),
                                html.P(
                                    """
                                    It does not feature a toroidal transformer for its electric isolation capabilities, rather it relies on passive means via varistors, gas discharge tubes, thermistors and voltage suppression components.
                                    The MCP500 unit short circuits when a certain threshold is reached so it is sacrificial to save the components that are connected to it. 
                                    """
                                    ,
                                    className = "mc500"
                                ),
                                html.P(
                                    """
                                   This system is not sacrificial and will not need replacing after a surge event. Isolation is the electrical or magnetic separation between two circuits and often used to separate two distinct sections of a power supply. The isolation provides a barrier across which dangerous voltages cannot pass in the event of a fault or component failure.

                                    """
                                    ,
                                    className = "mc1500"
                                ),
                                html.H3(
                                    """
                                    
                                    """,
                                    className = "space"

                                ),
                                html.H2(
                                    """
                                    MCP1500 and Niagara 7000

                                    """,
                                    className = "mcintosh"
                                ),
                                html.P(
                                    """
                                   The Niagara 7000 uses our patented AC Ground Noise-Dissipation System, the world’s first Dielectric-Biased AC Isolation Transformers, 
                                   and the widest bandwidth-linearized noise-dissipation circuit in the industry. Our unique passive/active Transient Power Correction Circuit features an instantaneous current reservoir of over 90 amps peak, specifically designed for today’s current-starved power amplifiers. Most AC power products featuring “high-current outlets” merely minimize current compression; the Niagara 7000 corrects it.

                                    """
                                ),
                                html.H5(
                                    """

                                    As seen in the picture on the Niagara 7000 page, it has about 7 toroidal isolation transformers. The description above declares it as a " Dielectric-Biased AC Isolation Transformer". A dielectric is the insulation material that is used in between the two walls of a toroid. This is the same component as the MCP1500. They are both AC isolation transformers that are non sacrificial.
                                    """
                                ),
                                 html.P(
                                    """

                                         To compare performance one online review said:
                                            "McIntosh MPC1500 was 0.6%, even better, and for the price it should be. 
                                    Audioquest Niagara 7000 was 0.0%-0.1%, but mostly 0.0%!"
                                    These numbers are regarding noise reduction, and the Niagara 7000 works better than the MCP1500.


                                    """
                                ),
                                html.H2(
                                    """
                                    McIntosh Units and Furman IT-REF 20I

                                    """,
                                    className = "mcintosh"
                                ),
                                 html.P(
                                    """
                                   Both the MCP500 and the Furman are power conditioners. But the Furman power conditioner also reduces noise in the AC power, as do the Power Isolaters, so that the audio and video are cleaner, more clear, and uncompromised.
                                   Also, the Furman is not sacrifical unlike the MCP500, and since it reduces noise in the AC power, it is more similar to the MCP1500 and Niagara 7000.

                                    """
                                ),
                                
                        ],
                        ),
                    ),
                ],
            )
        ],
    )

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
    ],
)

        

if __name__ == '__main__':
    app.run_server(debug=True)
