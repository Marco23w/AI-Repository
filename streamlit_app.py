import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Configurazione pagina
st.set_page_config(
    page_title="AssicuraTI - Calcolo Preventivo",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rileva il tema utilizzato (chiaro o scuro)
# Questa è una soluzione temporanea fino a quando Streamlit non fornirà un API per rilevare il tema
theme_css = """
<script>
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.add('light-theme');
    }
</script>
<style>
    .dark-theme { /* Nessuna modifica necessaria, già supportato */ }
    .light-theme { /* Necessarie modifiche per il tema chiaro */ }
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# CSS per rimuovere elementi di Streamlit e personalizzare lo stile
st.markdown("""
<style>
    /* Rimuovi elementi nativi di Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Variabili colori per supportare entrambi i temi */
    :root {
        --background-primary: #ffffff;
        --background-secondary: #f5f5f5;
        --background-card: #ffffff;
        --border-color: #e0e0e0;
        --text-primary: #333333;
        --text-secondary: #666666;
        --text-muted: #888888;
        --accent-primary: #1E88E5;
        --accent-secondary: #64B5F6;
        --accent-tertiary: #E3F2FD;
        --success: #43A047;
        --warning: #FB8C00;
        --danger: #E53935;
        --neutral: #78909C;
        --separator: #e0e0e0;
    }
    
    /* Override per tema scuro - viene applicato automaticamente in dark mode */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-primary: #121212;
            --background-secondary: #1e1e1e;
            --background-card: #242424;
            --border-color: #333333;
            --text-primary: #e0e0e0;
            --text-secondary: #b0b0b0;
            --text-muted: #808080;
            --accent-primary: #90CAF9;
            --accent-secondary: #64B5F6;
            --accent-tertiary: #0d47a1;
            --separator: #333333;
        }
    }
    
    /* Stile per le sezioni della sidebar */
    .sidebar-section {
        margin-top: 25px;
        margin-bottom: 10px;
    }
    
    /* Titoli delle sezioni */
    .section-title {
        font-weight: 600;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--text-secondary);
    }
    
    /* Separatori orizzontali */
    .separator {
        margin: 20px 0;
        border-top: 1px solid var(--separator);
    }
    
    /* Stile per label */
    .input-label {
        font-size: 14px;
        margin-bottom: 5px;
        color: var(--text-primary);
    }
    
    /* Pulsante calcola */
    .stButton>button {
        width: 100%;
        background-color: var(--accent-primary) !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 0.375rem 0.75rem !important;
    }
    
    /* Stile per radio button e select box */
    div[data-testid="stRadio"] > div {
        padding: 0;
    }
    
    /* Riduce lo spazio sopra/sotto agli slider */
    div[data-testid="stSlider"] {
        padding-top: 0;
        padding-bottom: 1rem;
    }
    
    /* Rimuovi il colore blu di sfondo dagli slider */
    .stSlider [data-baseweb="slider"] {
        background-color: var(--background-secondary) !important;
    }
    
    /* Stile header principale */
    .main-header {
        color: var(--accent-primary);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Stile per i risultati */
    .result-card {
        background-color: var(--background-card);
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .result-title {
        color: var(--accent-primary);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    .price-display {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--accent-primary);
        text-align: center;
        margin: 15px 0;
    }
    
    .price-info {
        color: var(--text-secondary);
        font-size: 1rem;
        text-align: center;
    }
    
    .monthly-price {
        font-size: 1.5rem;
        color: var(--accent-secondary);
        text-align: center;
        margin-top: 5px;
    }
    
    /* Stile per le schede informative */
    .info-section {
        margin-top: 30px;
    }
    
    .info-title {
        color: var(--accent-primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
        padding-bottom: 5px;
        border-bottom: 1px solid var(--separator);
    }
    
    .info-card {
        background-color: var(--background-card);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .factor-title {
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .factor-list {
        margin: 0;
        padding-left: 20px;
        color: var(--text-secondary);
    }
    
    .factor-list li {
        margin-bottom: 8px;
    }
    
    .comparison-bar {
        height: 24px;
        width: 100%;
        background-color: var(--background-secondary);
        border-radius: 4px;
        margin: 8px 0;
        position: relative;
        overflow: hidden;
    }
    
    .bar-fill {
        height: 100%;
        border-radius: 4px;
        padding-left: 8px;
        display: flex;
        align-items: center;
        color: white;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .bar-text-container {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 3px;
    }
    
    .footer {
        text-align: center;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid var(--separator);
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    
    /* Miglioramenti per sidebar */
    .sidebar .sidebar-content {
        background-color: var(--background-primary);
    }
    
    /* Miglioramenti specifici per tema chiaro */
    @media (prefers-color-scheme: light) {
        .stRadio > div {
            background-color: var(--background-card);
            border-radius: 5px;
            padding: 10px;
            border: 1px solid var(--border-color);
        }
        
        div[data-testid="stSelectbox"] > div {
            background-color: var(--background-card);
            border: 1px solid var(--border-color);
        }
    }
</style>
""", unsafe_allow_html=True)

# Funzione per ottenere i dati da input dell'utente
def get_input_data():
    with st.sidebar:
        # SEZIONE: DATI PERSONALI
        st.markdown('<div class="sidebar-section"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Dati Personali</div>', unsafe_allow_html=True)
        
        # Età
        st.markdown('<div class="input-label">Età</div>', unsafe_allow_html=True)
        eta = st.slider(" ", 18, 100, 30)
        
        # Sesso
        st.markdown('<div class="input-label">Sesso</div>', unsafe_allow_html=True)
        sex_ui = st.radio(" ", ["Maschio", "Femmina"], horizontal=True)
        
        # Peso
        st.markdown('<div class="input-label">Peso (kg)</div>', unsafe_allow_html=True)
        peso = st.slider("  ", 40, 150, 70)
        
        # Altezza
        st.markdown('<div class="input-label">Altezza (cm)</div>', unsafe_allow_html=True)
        altezza = st.slider("   ", 140, 210, 170)
        
        # Calcola BMI automaticamente (ma non lo mostriamo direttamente)
        altezza_m = altezza / 100
        bmi = round(peso / (altezza_m * altezza_m), 1)
        
        # Separatore
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # SEZIONE: FAMIGLIA
        st.markdown('<div class="section-title">👨‍👩‍👧‍👦 Famiglia</div>', unsafe_allow_html=True)
        
        # Numero figli
        st.markdown('<div class="input-label">Numero di figli a carico</div>', unsafe_allow_html=True)
        children = st.slider("    ", 0, 10, 0)
        
        # Separatore
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # SEZIONE: STILE DI VITA
        st.markdown('<div class="section-title">🔥 Stile di Vita</div>', unsafe_allow_html=True)
        
        # Fumatore
        st.markdown('<div class="input-label">Sei fumatore?</div>', unsafe_allow_html=True)
        smoker_ui = st.radio("     ", ["No", "Sì"], horizontal=True)
        
        # Separatore
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # SEZIONE: LOCALITÀ
        st.markdown('<div class="section-title">📍 Località</div>', unsafe_allow_html=True)
        
        # Regione
        st.markdown('<div class="input-label">Regione di residenza</div>', unsafe_allow_html=True)
        
        # Mappa regioni a nomi più comprensibili in italiano
        region_names = {
            "northeast": "Nord Est",
            "northwest": "Nord Ovest",
            "southeast": "Sud Est",
            "southwest": "Sud Ovest"
        }
        
        region_keys = list(region_names.keys())
        region_values = list(region_names.values())
        
        selected_region_idx = st.selectbox("      ", 
                               options=range(len(region_values)),
                               format_func=lambda x: region_values[x],
                               index=0)
        
        region = region_keys[selected_region_idx]
        
        # Separatore
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # Pulsante calcolo
        calculate_button = st.button('💲 Calcola Preventivo', use_container_width=True)
        
        # Mappa i valori dell'interfaccia utente ai valori originali del dataset
        sex = "female" if sex_ui == "Femmina" else "male"
        smoker = "yes" if smoker_ui == "Sì" else "no"
        
        # Trasformare i dati in un dizionario
        input_data = {
            "age": eta,
            "sex": sex,
            "bmi": bmi,  # Calcolato automaticamente
            "weight": peso,
            "height": altezza,
            "children": children,
            "smoker": smoker,
            "region": region
        }
        
    return pd.DataFrame([input_data]), input_data, calculate_button

# Funzione per una stima approssimativa
def estimate_premium(data):
    # Formula base simulata per una stima approssimativa
    age = data['age']
    bmi = data['bmi']
    children = data['children']
    smoker = data['smoker']
    
    base_premium = 5000
    age_factor = age * 50
    bmi_factor = max(0, (bmi - 20) * 500)
    children_factor = children * 800
    smoker_factor = 10000 if smoker == "yes" else 0
    
    return base_premium + age_factor + bmi_factor + children_factor + smoker_factor

# Funzione per visualizzare i fattori che influenzano il costo
def show_factors():
    st.markdown('<div class="info-title">Fattori che influenzano il costo</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="factor-title">🔥 Impatto elevato</div>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="factor-list">
            <li><strong>Essere fumatore</strong>: aumenta significativamente il costo (fino al 250%)</li>
            <li><strong>BMI elevato</strong>: ogni punto sopra 30 aumenta il costo</li>
            <li><strong>Età avanzata</strong>: il premio aumenta con l'età</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="factor-title">🔸 Impatto moderato</div>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="factor-list">
            <li><strong>Numero di figli</strong>: ogni figlio aumenta il costo</li>
            <li><strong>Regione di residenza</strong>: alcune regioni hanno costi più alti</li>
            <li><strong>Sesso</strong>: può influire sul costo in alcune regioni</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Funzione per mostrare suggerimenti per risparmiare
def show_saving_tips(data):
    st.markdown('<div class="info-title">Come risparmiare sul premio</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    
    tips = []
    
    if data['smoker'] == 'yes':
        tips.append("<li><strong>Smettere di fumare</strong> potrebbe ridurre il tuo premio fino al 70%</li>")
    
    if data['bmi'] > 25:
        tips.append("<li><strong>Ridurre il BMI</strong> sotto 25 potrebbe ridurre il premio fino al 30%</li>")
    
    tips.append("<li><strong>Confronta preventivi</strong> da diverse compagnie assicurative</li>")
    tips.append("<li><strong>Verifica sconti</strong> per pagamenti annuali o polizze multiple</li>")
    tips.append("<li><strong>Valuta franchigie più alte</strong> per abbassare il premio mensile</li>")
    
    st.markdown(f"""
    <ul class="factor-list">
        {"".join(tips)}
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Funzione per mostrare il confronto senza usare matplotlib
def show_comparison(prediction):
    st.markdown('<div class="info-title">Confronto con la media nazionale</div>', unsafe_allow_html=True)
    
    # Dati di esempio per il confronto
    avg_national = 8500  # esempio di media nazionale
    avg_nonsmoker = 6000  # esempio per non fumatori
    avg_smoker = 15000   # esempio per fumatori
    max_value = max(prediction, avg_national, avg_nonsmoker, avg_smoker)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    
    # Tuo preventivo
    percentage = min(100, int((prediction / max_value) * 100))
    st.markdown('<div class="bar-text-container"><div>Il tuo preventivo</div><div>$'+f"{prediction:.2f}"+'</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="comparison-bar"><div class="bar-fill" style="width: {percentage}%; background-color: #1E88E5;"></div></div>', unsafe_allow_html=True)
    
    # Media nazionale
    percentage = min(100, int((avg_national / max_value) * 100))
    st.markdown('<div class="bar-text-container"><div>Media nazionale</div><div>$'+f"{avg_national:.2f}"+'</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="comparison-bar"><div class="bar-fill" style="width: {percentage}%; background-color: #78909C;"></div></div>', unsafe_allow_html=True)
    
    # Media non fumatori
    percentage = min(100, int((avg_nonsmoker / max_value) * 100))
    st.markdown('<div class="bar-text-container"><div>Media non fumatori</div><div>$'+f"{avg_nonsmoker:.2f}"+'</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="comparison-bar"><div class="bar-fill" style="width: {percentage}%; background-color: #43A047;"></div></div>', unsafe_allow_html=True)
    
    # Media fumatori
    percentage = min(100, int((avg_smoker / max_value) * 100))
    st.markdown('<div class="bar-text-container"><div>Media fumatori</div><div>$'+f"{avg_smoker:.2f}"+'</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="comparison-bar"><div class="bar-fill" style="width: {percentage}%; background-color: #E53935;"></div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Funzione principale
def main():
    # Ottieni input
    input_df, input_data_raw, calculate_button = get_input_data()
    
    # Header
    st.markdown('<div class="main-header">💰 AssicuraTI - Calcola il tuo preventivo sanitario</div>', unsafe_allow_html=True)
    
    # Spiegazione iniziale
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    <p>La tua assicurazione sanitaria personalizzata, semplice e veloce.</p>
    <p>Questo strumento ti permette di ottenere un preventivo indicativo per la tua polizza sanitaria 
    in base alle tue caratteristiche personali.</p>
    <p><strong>Inserisci i tuoi dati nel pannello a sinistra e clicca su "Calcola Preventivo".</strong></p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Area per risultati
    if calculate_button:
        # Calcolo del preventivo
        with st.spinner('Calcoliamo il tuo preventivo personalizzato...'):
            try:
                # Prova a caricare il modello e fare la previsione
                model = joblib.load('gbr_model.pkl')
                scaler = joblib.load('scaler.pkl')
                
                # Prepara i dati
                age = input_data_raw['age']
                bmi = input_data_raw['bmi']
                children = input_data_raw['children']
                sex = input_data_raw['sex']
                smoker = input_data_raw['smoker']
                
                # Crea il dataframe con le feature
                processed_data = {
                    'age': age,
                    'bmi': bmi,
                    'children': children,
                    'sex_male': 1 if sex == 'male' else 0,
                    'smoker_yes': 1 if smoker == 'yes' else 0
                }
                
                input_data_processed = pd.DataFrame([processed_data])
                
                # Verifica se lo scaler ha feature names e fa reindex se necessario
                expected_columns = getattr(scaler, 'feature_names_in_', None)
                if expected_columns is not None:
                    input_data_processed = input_data_processed.reindex(columns=expected_columns, fill_value=0)
                
                # Preprocessing e previsione
                input_data_scaled = scaler.transform(input_data_processed)
                prediction = model.predict(input_data_scaled)[0]
                
            except Exception as e:
                # In caso di errore, usa la stima approssimativa
                prediction = estimate_premium(input_data_raw)
        
        # Mostra il risultato
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">Il tuo preventivo</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price-display">${prediction:.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="price-info">Premio annuale stimato</div>', unsafe_allow_html=True)
        
        monthly = prediction / 12
        st.markdown(f'<div class="monthly-price">${monthly:.2f} al mese</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sezione informativa
        st.markdown('<div class="info-section">', unsafe_allow_html=True)
        
        # Mostra le sezioni informative
        show_factors()
        show_saving_tips(input_data_raw)
        show_comparison(prediction)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">© 2025 AssicuraTI - Questo preventivo ha solo scopo dimostrativo e non costituisce un\'offerta contrattuale.</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
