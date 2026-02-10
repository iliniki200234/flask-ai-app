# Am(I)Hungry - Quick Start Guide

## Γρήγορη Εκκίνηση (5 λεπτά)

### Βήμα 1: Εγκατάσταση (ΗΔΗ ΟΛΟΚΛΗΡΩΘΗΚΕ ✓)

```bash
pip install Flask anthropic python-dotenv
```

### Βήμα 2: Ρύθμιση API Key

1. Πήγαινε στο https://console.anthropic.com/
2. Δημιούργησε λογαριασμό (δωρεάν)
3. Πάρε το API key σου
4. Άνοιξε το αρχείο `.env` και βάλε το key:

```
ANTHROPIC_API_KEY=sk-ant-api03-XXXXX...
```

### Βήμα 3: Εκκίνηση

**Windows:**
```bash
start.bat
```

**Ή χειροκίνητα:**
```bash
python database.py
python app.py
```

### Βήμα 4: Άνοιξε τον Browser

Πήγαινε στο: **http://localhost:5000**

---

## Τι μπορείς να κάνεις:

### 1. Ρώτα τον AI (Ελληνικά ή Αγγλικά):
- "Ποιο burger έχει καλύτερη τιμή στο efood vs wolt?"
- "Θέλω πίτσα κάτω από 10 ευρώ"
- "Ποιες είναι οι καλύτερες προσφορές;"
- "Σύγκρινε τα McNuggets"

### 2. Χρησιμοποίησε τα Φίλτρα:
- Επίλεξε κατηγορία (Burgers, Pizza, Sandwiches, κλπ)
- Επίλεξε πλατφόρμα (efood ή wolt)
- Όρισε μέγιστη τιμή
- Αναζήτηση με λέξη-κλειδί

### 3. Γρήγορες Ενέργειες:
- 🔥 Καλύτερες Προσφορές
- 📋 Όλα τα Προϊόντα
- 🔄 Σύγκριση Πλατφορμών
- 🏪 Εστιατόρια

---

## Dataset

Το σύστημα περιέχει **mock data**:
- 12 εστιατόρια (6 chains × 2 platforms)
- 48 προϊόντα
- Goody's, Everest, Pizza Fan, KFC, McDonald's, Subway

---

## Troubleshooting

### AI δεν δουλεύει;
➜ Βεβαιώσου ότι έβαλες το ANTHROPIC_API_KEY στο .env

### Port 5000 κατειλημμένο;
➜ Στο app.py γραμμή 200, άλλαξε σε: `app.run(debug=True, port=5001)`

### Database error;
➜ Διέγραψε το amiHungry.db και τρέξε: `python database.py`

---

## Δομή Αρχείων

```
iliana/
├── app.py              # Flask server
├── database.py         # Database setup
├── start.bat          # Windows startup script
├── .env               # API keys (ΣΥΜΠΛΗΡΩΣΕ ΑΥΤΟ!)
├── requirements.txt   # Dependencies
└── static/
    ├── index.html     # Frontend
    ├── styles.css     # Styling
    └── script.js      # JavaScript
```

---

**Έτοιμο! Απόλαυσε τον AI πράκτορα σου! 🍔🚀**
