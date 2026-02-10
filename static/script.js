// arxikopoiisi otan fortonei i selida
document.addEventListener('DOMContentLoaded', function() {
    fortomaStatistika();
});

// fortoma statistikon
async function fortomaStatistika() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;
            const statsHTML = `
                <span class="stat-item">📦 ${stats.total_products} Προϊόντα</span>
                <span class="stat-item">🏪 ${stats.total_restaurants} Εστιατόρια</span>
                <span class="stat-item">🔥 ${stats.products_with_offers} Προσφορές</span>
                <span class="stat-item">💰 €${stats.price_range.min} - €${stats.price_range.max}</span>
                <span class="stat-item">📊 Μέση τιμή: €${stats.price_range.avg}</span>
            `;
            document.getElementById('statsBar').innerHTML = statsHTML;
        }
    } catch (error) {
        console.error('error sto fortoma stats:', error);
    }
}

// xeirisi enter key sto chat
function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        rotaAI();
    }
}

// rotisi ston ai agent
async function rotaAI() {
    const input = document.getElementById('chatInput');
    const erotisi = input.value.trim();

    if (!erotisi) {
        alert('Παρακαλώ πληκτρολόγησε μια ερώτηση!');
        return;
    }

    const chatBox = document.getElementById('chatBox');
    const loading = document.getElementById('chatLoading');

    // prosthiki minyma xristi
    const userMessageHTML = `
        <div class="chat-message user-message">
            <strong>Εσύ:</strong> ${escapeHtml(erotisi)}
        </div>
    `;
    chatBox.innerHTML += userMessageHTML;
    chatBox.scrollTop = chatBox.scrollHeight;

    // katharismo input kai emfanisi loading
    input.value = '';
    loading.style.display = 'flex';

    try {
        const response = await fetch('/api/ask-ai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: erotisi })
        });

        const data = await response.json();
        loading.style.display = 'none';

        if (data.success) {
            // morfopoiisi apantisis ai
            let morfopoiimeniApantisi = morfopoiisiApantisi(data.answer);

            // προσθηκη notice αν υπαρχουν προτεινομενα
            if (data.recommended_products && data.recommended_products.length > 0) {
                morfopoiimeniApantisi += `
                    <div class="recommendations-notice">
                        <div class="recommendations-icon">👇</div>
                        <div class="recommendations-text">
                            Δείτε πιο κάτω στα <a href="#proteinomenaSection" style="color: var(--secondary-color); font-weight: bold; text-decoration: none;">Προτεινόμενα Προϊόντα</a> τις επιλογές που ανέφερα!
                        </div>
                    </div>
                `;
            }

            const aiMessageHTML = `
                <div class="chat-message ai-message">
                    <strong>AI Agent:</strong>
                    <div class="ai-response-content">${morfopoiimeniApantisi}</div>
                </div>
            `;
            chatBox.innerHTML += aiMessageHTML;

            // an yparxoun proteinomena proionta, na ta deixei
            if (data.recommended_products && data.recommended_products.length > 0) {
                deixeProionta(data.recommended_products, `💡 Προτεινόμενα Προϊόντα (${data.recommended_products.length})`);
            }
        } else {
            const errorHTML = `
                <div class="chat-message ai-message">
                    <strong>AI Agent:</strong> ⚠️ Σφάλμα: ${escapeHtml(data.error)}
                    <br><br>
                    💡 Βεβαιώσου ότι έχεις ρυθμίσει το OPENROUTER_API_KEY στο αρχείο .env
                </div>
            `;
            chatBox.innerHTML += errorHTML;
        }

        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        loading.style.display = 'none';
        console.error('error sti rotisi ai:', error);
        alert('Σφάλμα επικοινωνίας με τον AI πράκτορα!');
    }
}

// emfanisi kalyterон prosfores
async function showBestOffers() {
    try {
        const response = await fetch('/api/best-offers');
        const data = await response.json();

        if (data.success) {
            deixeProionta(data.data, `🔥 Καλύτερες Προσφορές (${data.total_offers})`);
        }
    } catch (error) {
        console.error('error sto fortoma prosfores:', error);
        alert('Σφάλμα φόρτωσης προσφορών!');
    }
}

// emfanisi olon ton proionton
async function showAllProducts() {
    try {
        const response = await fetch('/api/products');
        const data = await response.json();

        if (data.success) {
            deixeProionta(data.data, `📋 Όλα τα Προϊόντα (${data.data.length})`);
        }
    } catch (error) {
        console.error('error sto fortoma proionton:', error);
        alert('Σφάλμα φόρτωσης προϊόντων!');
    }
}

// sigkrisi platform
async function comparePlatforms() {
    const onoma = prompt('Εισήγαγε όνομα προϊόντος για σύγκριση (π.χ. "Big Mac"):');

    if (!onoma) return;

    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_name: onoma })
        });

        const data = await response.json();

        if (data.success) {
            if (data.data.length === 0) {
                alert('Δεν βρέθηκαν προϊόντα για σύγκριση!');
                return;
            }
            deixeSigkriseis(data.data);
        }
    } catch (error) {
        console.error('error sti sigkrisi:', error);
        alert('Σφάλμα σύγκρισης!');
    }
}

// emfanisi estiaторion
async function showRestaurants() {
    try {
        const response = await fetch('/api/restaurants');
        const data = await response.json();

        if (data.success) {
            deixeEstiatoria(data.data);
        }
    } catch (error) {
        console.error('error sto fortoma estiatorion:', error);
        alert('Σφάλμα φόρτωσης εστιατορίων!');
    }
}

// efarmogi filtron
async function applyFilters() {
    const katigoria = document.getElementById('categoryFilter').value;
    const platform = document.getElementById('platformFilter').value;
    const maxTimi = document.getElementById('maxPriceFilter').value;
    const anaζitisi = document.getElementById('searchFilter').value;

    const params = new URLSearchParams();
    if (katigoria) params.append('category', katigoria);
    if (platform) params.append('platform', platform);
    if (maxTimi) params.append('max_price', maxTimi);
    if (anaζitisi) params.append('query', anaζitisi);

    try {
        const response = await fetch(`/api/products?${params.toString()}`);
        const data = await response.json();

        if (data.success) {
            deixeProionta(data.data, `🔍 Αποτελέσματα Φίλτρων (${data.data.length})`);
        }
    } catch (error) {
        console.error('error sti efarmogi filtron:', error);
        alert('Σφάλμα εφαρμογής φίλτρων!');
    }
}

// katharismo filtron
function resetFilters() {
    document.getElementById('categoryFilter').value = '';
    document.getElementById('platformFilter').value = '';
    document.getElementById('maxPriceFilter').value = '';
    document.getElementById('searchFilter').value = '';

    document.getElementById('resultsContainer').innerHTML = `
        <div class="empty-state">
            <p>Χρησιμοποίησε τα φίλτρα ή ρώτησε τον AI πράκτορα για να δεις αποτελέσματα!</p>
        </div>
    `;
    document.getElementById('resultsTitle').textContent = '📊 Αποτελέσματα';
}

// emfanisi proionton
function deixeProionta(proionta, titlos) {
    document.getElementById('resultsTitle').textContent = titlos;

    if (proionta.length === 0) {
        document.getElementById('resultsContainer').innerHTML = `
            <div class="empty-state">
                <p>Δεν βρέθηκαν προϊόντα!</p>
            </div>
        `;
        return;
    }

    const productsHTML = proionta.map(product => {
        const exeiProsfora = product.has_offer;
        const telikitimi = exeiProsfora ? product.offer_price : product.price;
        const eksikonomisi = exeiProsfora ? (product.price - product.offer_price).toFixed(2) : 0;

        return `
            <div class="product-card">
                <div class="product-header">
                    <div>
                        <div class="product-name">${escapeHtml(product.name)}</div>
                        <div class="product-restaurant">
                            ${escapeHtml(product.restaurant_name)}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        ${exeiProsfora ? `<div class="price-original">€${product.price}</div>` : ''}
                        <div class="product-price">€${telikitimi}</div>
                    </div>
                </div>

                <div class="product-description">
                    ${escapeHtml(product.description || '')}
                </div>

                <div class="product-tags">
                    <span class="tag tag-platform">${escapeHtml(product.platform)}</span>
                    <span class="tag tag-category">${escapeHtml(product.category)}</span>
                    ${exeiProsfora ? `<span class="tag tag-offer">🔥 -€${eksikonomisi}</span>` : ''}
                </div>

                <div class="product-info">
                    <span>⭐ ${product.rating}</span>
                    <span>🚚 ${product.delivery_time_min}-${product.delivery_time_max} λεπτά</span>
                    <span>🍽️ ${product.calories || '?'} cal</span>
                </div>

                ${exeiProsfora ? `
                    <div style="margin-top: 10px; padding: 10px; background: rgba(76, 175, 80, 0.2); border-radius: 5px; text-align: center; color: var(--success-color); font-weight: 600;">
                        ${escapeHtml(product.offer_description)}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');

    document.getElementById('resultsContainer').innerHTML = productsHTML;
}

// emfanisi sigkriseon
function deixeSigkriseis(sigkriseis) {
    document.getElementById('resultsTitle').textContent = `🔄 Σύγκριση Πλατφορμών (${sigkriseis.length})`;

    const comparisonsHTML = sigkriseis.map(comp => {
        const efood = comp.efood;
        const wolt = comp.wolt;
        const fthinoteri = comp.cheaper_platform;

        return `
            <div class="comparison-card">
                <div class="comparison-header">
                    <div class="comparison-title">${escapeHtml(comp.product_name)}</div>
                    <div style="color: var(--text-secondary); font-size: 0.9em;">
                        ${escapeHtml(efood.restaurant_name)}
                    </div>
                </div>

                <div class="comparison-platforms">
                    <div class="platform-item ${fthinoteri === 'efood' ? 'winner' : ''}">
                        <div class="platform-name">🅴 efood ${fthinoteri === 'efood' ? '✓' : ''}</div>
                        <div style="font-size: 1.5em; font-weight: 700; color: var(--success-color); margin: 10px 0;">
                            €${efood.price}
                        </div>
                        <div style="color: var(--text-secondary); font-size: 0.9em;">
                            🚚 ${efood.delivery_time_min}-${efood.delivery_time_max} min<br>
                            📦 Κόστος: €${efood.delivery_fee}<br>
                            💳 Ελάχιστο: €${efood.minimum_order}
                        </div>
                    </div>

                    <div class="platform-item ${fthinoteri === 'wolt' ? 'winner' : ''}">
                        <div class="platform-name">🅦 wolt ${fthinoteri === 'wolt' ? '✓' : ''}</div>
                        <div style="font-size: 1.5em; font-weight: 700; color: var(--success-color); margin: 10px 0;">
                            €${wolt.price}
                        </div>
                        <div style="color: var(--text-secondary); font-size: 0.9em;">
                            🚚 ${wolt.delivery_time_min}-${wolt.delivery_time_max} min<br>
                            📦 Κόστος: €${wolt.delivery_fee}<br>
                            💳 Ελάχιστο: €${wolt.minimum_order}
                        </div>
                    </div>
                </div>

                <div class="comparison-savings">
                    💰 Εξοικονόμηση: €${comp.savings} στο ${fthinoteri}
                </div>
            </div>
        `;
    }).join('');

    document.getElementById('resultsContainer').innerHTML = comparisonsHTML;
}

// emfanisi estiatorion
function deixeEstiatoria(estiatoria) {
    document.getElementById('resultsTitle').textContent = `🏪 Εστιατόρια (${estiatoria.length})`;

    // omadopoiisi ana onoma
    const omadopoiimena = {};
    estiatoria.forEach(r => {
        if (!omadopoiimena[r.name]) {
            omadopoiimena[r.name] = [];
        }
        omadopoiimena[r.name].push(r);
    });

    const restaurantsHTML = Object.entries(omadopoiimena).map(([onoma, items]) => {
        return `
            <div class="product-card">
                <div class="product-name" style="margin-bottom: 15px;">${escapeHtml(onoma)}</div>
                <div style="color: var(--text-secondary); margin-bottom: 10px;">
                    ${escapeHtml(items[0].cuisine_type)} | ⭐ ${items[0].rating}
                </div>

                ${items.map(r => `
                    <div style="background: var(--card-bg); padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 3px solid ${r.platform === 'efood' ? '#FF6B35' : '#00D9FF'};">
                        <div style="font-weight: 700; color: var(--secondary-color); margin-bottom: 8px;">
                            ${r.platform === 'efood' ? '🅴' : '🅦'} ${escapeHtml(r.platform)}
                        </div>
                        <div style="font-size: 0.9em; color: var(--text-secondary);">
                            🚚 Παράδοση: ${r.delivery_time_min}-${r.delivery_time_max} λεπτά<br>
                            📦 Κόστος: €${r.delivery_fee}<br>
                            💳 Ελάχιστη παραγγελία: €${r.minimum_order}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }).join('');

    document.getElementById('resultsContainer').innerHTML = restaurantsHTML;
}

// morfopoiisi apantisis ai
function morfopoiisiApantisi(keimeno) {
    let morfopoiimeno = '';

    // xorisma se grammes
    const grammes = keimeno.split('\n');
    let seLista = false;

    grammes.forEach(grammi => {
        grammi = grammi.trim();

        if (grammi === '') {
            if (seLista) {
                morfopoiimeno += '</ul>';
                seLista = false;
            }
            morfopoiimeno += '<br>';
            return;
        }

        // elegxos an arxizei me koukida i arithmo
        if (grammi.match(/^[-•*]\s/) || grammi.match(/^\d+\.\s/)) {
            if (!seLista) {
                morfopoiimeno += '<ul class="ai-list">';
                seLista = true;
            }
            // afairesi koukidas kai morfopoiisi
            let periexomeno = grammi.replace(/^[-•*]\s/, '').replace(/^\d+\.\s/, '');
            // metatropi **text** se bold
            periexomeno = periexomeno.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            morfopoiimeno += `<li>${periexomeno}</li>`;
        } else {
            if (seLista) {
                morfopoiimeno += '</ul>';
                seLista = false;
            }
            // metatropi **text** se bold se paragrafous
            let periexomeno = grammi.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            morfopoiimeno += `<p class="ai-paragraph">${periexomeno}</p>`;
        }
    });

    if (seLista) {
        morfopoiimeno += '</ul>';
    }

    return morfopoiimeno;
}

// diafygi html
function escapeHtml(keimeno) {
    const div = document.createElement('div');
    div.textContent = keimeno;
    return div.innerHTML;
}
