import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle

st.title('Классификатор пингвинов')
st.write('Дополнительная информация')

df = pd.read_csv('penguins.csv')
rf_pickle = open('random_forest_penguin.pickle','rb')
map_pickle = open('output_penguin.pickle','rb')
rfc = pickle.load(rf_pickle)
unique_penguin_mapping = pickle.load(map_pickle)
rf_pickle.close()
map_pickle.close()

with st.form('пользовательские вводы'):
    island = st.selectbox('Остров проживания пингвинов',
                      options=['Biscoe','Dream','Torgerson'])
    sex = st.selectbox(
        'Пол', options=['Женская особь','Мужская особь',])
    bill_length = st.number_input('Длина_клюва_мм', min_value=0)
    bill_depth = st.number_input('Высота_клюва_мм', min_value=0)
    flipper_length = st.number_input('Длина ласт (мм)', min_value=0)
    body_mass = st.number_input('Масса тела (г)', min_value=0)
    st.form_submit_button()

island_biscoe, island_dream, island_torgerson = 0, 0, 0
if island == 'Biscoe':
    island_biscoe = 1
elif island == 'Dream':
    island_dream = 1
elif island == 'Torgerson':
    island_torgerson = 1
sex_famale, sex_male = 0, 0
if sex == 'Женская особь':
    sex_famale = 1
elif sex == 'Мужская особь':
    sex_male = 1

new_prediction = rfc.predict([[bill_length, 
                               bill_depth, 
                               flipper_length, 
                               body_mass, 
                               island_biscoe, 
                               island_dream, 
                               island_torgerson, 
                               sex_famale, 
                               sex_male]])

prediction_species = unique_penguin_mapping[new_prediction][0]
st.subheader('Прогнозирование вида пингвина')
st.write('Мы прогнозируем, что ваш пингвин относится к виду {}'.format(prediction_species))

st.image('feature_importances.png')
st.write('Ниже приведены распределений трёх переменных')

fig, ax = plt.subplots()
ax = sns.displot(x=df['длина_клюва_мм'], hue=df['вид'])
plt.axvline(bill_length)
plt.title('Распределение длины клюва по видам пингвинов')
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=df['высота_клюва_мм'], hue=df['вид'])
plt.axvline(bill_depth)
plt.title('Распределение высоты клюва по видам пингвинов')
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=df['длина_ласт_мм'], hue=df['вид'])
plt.axvline(flipper_length)
plt.title('Распределение длины ласт по видам пингвинов')
st.pyplot(ax)

