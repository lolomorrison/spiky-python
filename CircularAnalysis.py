#Importing
import streamlit as st #Website App
import random #Python lib
from matplotlib import pyplot as plt #Pie Chart
import cohere #AI

co = cohere.Client('zysanKC01CGpWAZKsbXi5jB3q07QvqWaGPjifNec') #Cohere API key

st.set_page_config(layout = "wide") #Making use of the whole page

default_values = { #setting the default values of the sliders
    "mass": 0.5,
    "rec_feed": 0.5,
    "reuse_feed": 0.5,
    "reuse_col": 0.33,
    "rec_col": 0.33
}

product_name = ''
product_lifetime = 0

everything = st.empty() #creating a container that can be cleared
everything_sidebar = st.sidebar.empty() #creating a container that can be cleared


if "materials" not in st.session_state: #initializing the materials variable
    st.session_state.materials = []

if "material_values" not in st.session_state: #initializing the material values dictionary
    st.session_state.material_values = {}

if "start_screen" not in st.session_state:
    st.session_state.start_screen = True

if "choice_index" not in st.session_state:
    st.session_state.choice_index = 0

def random_color_gen():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return [r,g,b]

def starting_input():
    if st.session_state.product_name and st.session_state.product_lifetime:
        global product_name
        global product_lifetime
        st.session_state.saved_name = st.session_state.product_name
        st.session_state.saved_life = st.session_state.product_lifetime
        st.session_state.start_screen = False
        starting_screen.empty()
    else:
        st.error("Please fill out the required fields")

def add_material(): #function that triggers when the user adds a material
    if st.session_state.enter not in st.session_state.materials:
        st.session_state.materials.append(st.session_state.enter)
        st.session_state.material_values[st.session_state.enter] = default_values
        st.session_state.enter = ''
        for x in range(0, len(st.session_state.materials)):
            if st.session_state.choice == st.session_state.materials[x]:
                st.session_state.choice_index = x

def sync_to_session_state(): #function that triggers when the user chnages the material selected

    slider_values =  { #recording the slider values
    "mass": st.session_state.mass_input,
    "rec_feed": st.session_state.rec_feed,
    "reuse_feed": st.session_state.reuse_feed,
    "reuse_col": st.session_state.rec_col,
    "rec_col": st.session_state.reuse_col
    #"comp_col": st.session_state.comp_col
}

    st.session_state.material_values[material_choice] = slider_values #copying the slider values to session state

    if not calculate_button:
        #setting slider values to the session state of the new material
        st.session_state.mass_input = st.session_state.material_values[st.session_state.choice]['mass']
        st.session_state.rec_feed = st.session_state.material_values[st.session_state.choice]['rec_feed']
        st.session_state.reuse_feed = st.session_state.material_values[st.session_state.choice]['reuse_feed']
        st.session_state.rec_col = st.session_state.material_values[st.session_state.choice]['rec_col']
        st.session_state.reuse_col = st.session_state.material_values[st.session_state.choice]['reuse_col']
        #st.session_state.comp_col = st.session_state.material_values[st.session_state.choice]['comp_col']

with everything_sidebar.container():
    if not st.session_state.start_screen:
        material = st.text_input("Material Name", key='enter', on_change=add_material)

        material_choice = st.selectbox("Material", st.session_state.materials, on_change=sync_to_session_state,
                                       key='choice', index = st.session_state.choice_index)

        calculate_button = st.button("Calculate!")

with everything.container():
    if not st.session_state.start_screen:
        if st.session_state.choice:
            st.title(st.session_state.choice)

            st.number_input("Mass of Product (grams)", step=1.0,
                            value=0.5, key='mass_input')
            st.slider("Fraction of Recycled Feedstock", min_value=0.0, max_value=1.0,
                      value=0.5,
                      key='rec_feed')
            st.slider("Fraction of Reused Feedstock", min_value=0.0, max_value=1.0,
                      value=0.5,
                      key='reuse_feed')
            st.slider("Fraction of Mass Collected for Recycling", min_value=0.0, max_value=1.0,
                      value=0.33,
                      key='rec_col')
            st.slider("Fraction of Mass Collected for Reuse", min_value=0.0, max_value=1.0,
                      value=0.33,
                      key='reuse_col')
            #st.slider("Fraction of Mass Collected for Composting", min_value=0.0,
             #         max_value=1.0, value=0.33,
             #         key='comp_col')
        else:
            st.title("Please Enter A Material")

    else:
        st.title("Please Enter Your Product")
        starting_screen = st.empty()
        with starting_screen:
            with st.form("form"):
                st.text_input("Product Type", key = 'product_name')
                st.number_input("Product Lifetime (in years)", step = 1.0, key = 'product_lifetime')

                submit = st.form_submit_button("Submit", on_click = starting_input)

if not st.session_state.start_screen:
    if calculate_button:
        sync_to_session_state() #syncing any final changes user might've made

        #deleting the widgets
        everything.empty()
        everything_sidebar.empty()

        #initializing dictionaries to be used in calculations
        material_mass_dict = {}
        virgin_material_dict = {}
        combined_recycling_waste_dict = {}
        absolute_waste_dict = {}

        for i in range(len(st.session_state.materials)):
            # assigning variables to input dictionaries
            material_mass = st.session_state.material_values[st.session_state.materials[i]]["mass"]
            material_reuse_feedstock = st.session_state.material_values[st.session_state.materials[i]][
                "reuse_feed"]
            material_rec_feedstock = st.session_state.material_values[st.session_state.materials[i]]["rec_feed"]
            material_rec_collection = st.session_state.material_values[st.session_state.materials[i]][
                "rec_col"]
            #material_comp_collection = st.session_state.material_values[st.session_state.materials[i]][
             #   "comp_col"]
            material_reuse_collection = st.session_state.material_values[st.session_state.materials[i]][
                "reuse_col"]

            # AI calculation for recycling rate
            rec_response = co.chat(
                model='command-r-plus',
                message=f"Return only the recovery rate of \
                            {st.session_state.materials[i]} \
                            as a decimal. No words or explanation. If it is a range, return the average. \
                            For example, if the response is 0.87-0.91, return 0.89",
                prompt_truncation='AUTO',
                connectors=[{"id": "web-search"}])

            recycling_efficiency = float(rec_response.text)

            #debugging
            #with st.sidebar:
                #if rec_response:
                    #st.write(rec_response.text)

            # calculating equation variables from raw data
            virgin_material_calculation = material_mass * (1 - material_reuse_feedstock - material_rec_feedstock)
            unrecoverable_waste_calculation = material_mass * (
                    1 - material_rec_collection - material_reuse_collection)
            recycling_waste_collection_calculation = material_mass * (
                    1 - recycling_efficiency) * material_rec_collection
            recycling_waste_feedstock_calculation = material_mass * (
                    (1 - recycling_efficiency) * material_rec_feedstock) / recycling_efficiency

            combined_recycling_waste_calculation = (
                                                           recycling_waste_collection_calculation + recycling_waste_feedstock_calculation) / 2
            absolute_waste_calculation = unrecoverable_waste_calculation + combined_recycling_waste_calculation

            # storing calculations from each iteration in dictionaries
            combined_recycling_waste_dict.update({st.session_state.materials[i]: combined_recycling_waste_calculation})
            material_mass_dict.update({st.session_state.materials[i]: material_mass})
            virgin_material_dict.update({st.session_state.materials[i]: virgin_material_calculation})
            absolute_waste_dict.update({st.session_state.materials[i]: absolute_waste_calculation})

            # storing final sum of calculations in single variable
        material_mass_total = sum(material_mass_dict.values())
        combined_recycling_waste_total = sum(combined_recycling_waste_dict.values())
        virgin_material_total = sum(virgin_material_dict.values())
        absolute_waste_total = sum(absolute_waste_dict.values())

        life_response = co.chat(
            model='command-r-plus',
            message=f"Return the average lifetime in years for a \
            {st.session_state.saved_name} \
            as a number. No words or explanation. If it is a range, return the average.",
            prompt_truncation='AUTO',
            connectors=[{"id": "web-search"}]
        )

        linear_flow_index = (virgin_material_total + absolute_waste_total) / (
                    2 * material_mass_total + combined_recycling_waste_total)

        utility_factor = st.session_state.saved_life / float(life_response.text)
        utility_function = 0.9 / utility_factor

        material_circularity_index = 1 - (linear_flow_index * utility_function)

        # pie chart
        col1, col2, col3 = st.columns([1,2,1])
        pie_values = [material_circularity_index, 1 - material_circularity_index]
        pie_labels = ['Final Score', ' ']
        color = [0.06, 0.06, 0.09]
        circle = plt.Circle((0, 0), 0.75, color=color)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(tuple(color))
        with col2:
            ax.pie(pie_values, labels=pie_labels, startangle=90, counterclock=True, colors=['mediumseagreen', color], textprops={'color':"w"})
            ax.add_artist(circle)
            plt.text(-0.3, -0.175, str(round(material_circularity_index * 100)), color=(1, 1, 1), fontsize=50)
            st.pyplot(fig)
        #st.write(st.session_state)