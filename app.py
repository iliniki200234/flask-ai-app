from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from database import init_database, get_all_products, search_products, get_all_restaurants

# fortosi metavliton perivallontos
load_dotenv()

app = Flask(__name__, static_folder='static')
@app.route("/")
def home():
    return "OK - app is running"
# arxikopoiisi openrouter ai client
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
AI_ENABLED = bool(OPENROUTER_API_KEY)

if AI_ENABLED:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )
else:
    print("warning: openrouter ai den exei rythmistei. prosthese OPENROUTER_API_KEY sto .env")

# arxikopoiisi vasis dedomενon
#try:
#    init_database()
#except Exception as e:
#    print(f"i vasi exei idi arxikopoiithei i error: {e}")

@app.route('/')
def index():
    # epistrofi kyrias selidas
    return send_from_directory('static', 'index.html')

@app.route('/api/restaurants', methods=['GET'])
def parne_estiatoria():
    # epistrofi olon ton estiatorion
    try:
        estiatoria = get_all_restaurants()
        return jsonify({'success': True, 'data': estiatoria})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def parne_proionta():
    # epistrofi olon ton proionton i me filtra
    try:
        erotima = request.args.get('query')
        katigoria = request.args.get('category')
        max_timi = request.args.get('max_price')
        platform = request.args.get('platform')

        if any([erotima, katigoria, max_timi, platform]):
            proionta = search_products(erotima, katigoria, max_timi, platform)
        else:
            proionta = get_all_products()

        return jsonify({'success': True, 'data': proionta})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ask-ai', methods=['POST'])
def rota_ai():
    # rotisi ston ai agent gia protaseis fagitou
    if not AI_ENABLED:
        return jsonify({
            'success': False,
            'error': 'ai den exei rythmistei. prosthese OPENROUTER_API_KEY sto .env'
        }), 500

    try:
        data = request.json
        erotisi_xristi = data.get('question', '')

        if not erotisi_xristi:
            return jsonify({'success': False, 'error': 'den dothike erotisi'}), 400

        # pairnoume sxetika proionta me vasi tin erotisi gia context
        proionta = search_products(query=erotisi_xristi)

        # an den vrethike tipota, tote pairnoume ola (fallback)
        if not proionta:
           proionta = get_all_products()
        estiatoria = get_all_restaurants()

        # etoimasia context gia ai
        context = f"""
You are A(m)IHungry AI Agent, an intelligent food delivery assistant for Greek market.

Available Data:
- {len(estiatoria)} restaurants across efood and wolt platforms
- {len(proionta)} food products

Products Database (JSON format):
{json.dumps(proionta[:20], ensure_ascii=False, indent=2)}
... (showing first 20 products)

Your task:
- Analyze user questions in Greek or English
- Compare prices across platforms (efood vs wolt)
- Recommend best deals considering: price, delivery time, offers, ratings
- Provide specific product names, prices, and restaurant info
- Be concise but informative
- Always mention platform differences when relevant

User Question: {erotisi_xristi}
"""

        # Call OpenRouter AI using OpenAI SDK
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "AmIHungry AI Agent",
            },
            model="moonshotai/kimi-k2",
            messages=[
                {
                    "role": "user",
                    "content": context
                }
            ]
        )

        apantisi_ai = completion.choices[0].message.content

        # prospatheia eksagogis proteinomenon proionton apo tin apantisi
        proteinomena_proionta = []
        apantisi_mikra = apantisi_ai.lower()

        # eksagogi lekseon kleidion apo tin erotisi
        erotisi_mikra = erotisi_xristi.lower()

        # koines lekseis fagitou
        lekseis_fagitou = ['burger', 'pizza', 'sandwich', 'chicken', 'salad']

        # prospatheia na vroume proionta pou anaferθikan i tairiazoun
        for proion in proionta:
            onoma_proiontos_mikra = proion['name'].lower()

            # elegxos an to proion anaferetai sto onoma stin apantisi
            if onoma_proiontos_mikra in apantisi_mikra:
                if proion not in proteinomena_proionta:
                    proteinomena_proionta.append(proion)
            # i an tairiazei me lekseis kleidia apo tin erotisi
            elif any(leksi in erotisi_mikra and leksi in onoma_proiontos_mikra for leksi in lekseis_fagitou):
                if proion not in proteinomena_proionta:
                    proteinomena_proionta.append(proion)

            if len(proteinomena_proionta) >= 6:  # periorism os se 6 proionta
                break

        return jsonify({
            'success': True,
            'answer': apantisi_ai,
            'context_products_count': len(proionta),
            'recommended_products': proteinomena_proionta
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f"error: {str(e)}"}), 500

@app.route('/api/compare', methods=['POST'])
def sigkrisi_proionton():
    # sigkrisi proionton metaksy platform
    try:
        data = request.json
        onoma_proiontos = data.get('product_name', '')

        if not onoma_proiontos:
            return jsonify({'success': False, 'error': 'den dothike onoma proiontos'}), 400

        # anaζitisi paromoion proionton
        proionta = search_products(query=onoma_proiontos)

        if not proionta:
            return jsonify({
                'success': True,
                'data': [],
                'message': 'den vrethikan proionta'
            })

        # omadopoiisi ana onoma kai sigkrisi platform
        sigkrisi = {}
        for proion in proionta:
            klidi = proion['name']
            if klidi not in sigkrisi:
                sigkrisi[klidi] = []
            sigkrisi[klidi].append(proion)

        # ypologismos kalyteron symforon
        apotelesmata = []
        for onoma_proiontos, antikeimena in sigkrisi.items():
            if len(antikeimena) > 1:  # pollapla platforms
                efood_item = next((x for x in antikeimena if x['platform'] == 'efood'), None)
                wolt_item = next((x for x in antikeimena if x['platform'] == 'wolt'), None)

                if efood_item and wolt_item:
                    diafora_timis = abs(efood_item['price'] - wolt_item['price'])
                    fthinoteri_platforma = 'efood' if efood_item['price'] < wolt_item['price'] else 'wolt'

                    apotelesmata.append({
                        'product_name': onoma_proiontos,
                        'efood': efood_item,
                        'wolt': wolt_item,
                        'price_difference': round(diafora_timis, 2),
                        'cheaper_platform': fthinoteri_platforma,
                        'savings': round(diafora_timis, 2)
                    })

        return jsonify({
            'success': True,
            'data': apotelesmata,
            'total_comparisons': len(apotelesmata)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/best-offers', methods=['GET'])
def parne_kalyteres_prosfores():
    # epistrofi proionton me energes prosfores
    try:
        proionta = get_all_products()
        prosfores = [p for p in proionta if p['has_offer']]

        # ypologismos eksikonomisis
        for prosfora in prosfores:
            prosfora['savings'] = round(prosfora['price'] - prosfora['offer_price'], 2)
            prosfora['discount_percent'] = round((prosfora['savings'] / prosfora['price']) * 100, 1)

        # taksinomisi ana eksikonomisi
        prosfores.sort(key=lambda x: x['savings'], reverse=True)

        return jsonify({
            'success': True,
            'data': prosfores,
            'total_offers': len(prosfores)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def parne_statistika():
    # epistrofi statistikon vasis
    try:
        proionta = get_all_products()
        estiatoria = get_all_restaurants()

        # ypologismos statistikon
        synolo_proionton = len(proionta)
        synolo_estiatorion = len(estiatoria)
        proionta_me_prosfores = len([p for p in proionta if p['has_offer']])

        platframes = set(r['platform'] for r in estiatoria)
        katigories = set(p['category'] for p in proionta)

        mesi_timi = sum(p['price'] for p in proionta) / synolo_proionton if synolo_proionton > 0 else 0
        min_timi = min(p['price'] for p in proionta) if synolo_proionton > 0 else 0
        max_timi = max(p['price'] for p in proionta) if synolo_proionton > 0 else 0

        return jsonify({
            'success': True,
            'stats': {
                'total_products': synolo_proionton,
                'total_restaurants': synolo_estiatorion,
                'products_with_offers': proionta_me_prosfores,
                'platforms': list(platframes),
                'categories': list(katigories),
                'price_range': {
                    'min': round(min_timi, 2),
                    'max': round(max_timi, 2),
                    'avg': round(mesi_timi, 2)
                }
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("A(m)IHungry AI Agent - Food Delivery Assistant")
    print("=" * 60)
    print(f"AI Status: {'Enabled' if AI_ENABLED else 'Disabled - Set ANTHROPIC_API_KEY'}")
    print("Server starting on http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
