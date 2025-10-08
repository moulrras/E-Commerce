document.addEventListener('DOMContentLoaded', () => {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    const contadorCarrinho = document.getElementById('contador-carrinho');
    const carrinhoItensContainer = document.getElementById('itens-carrinho');
    const carrinhoTotalValor = document.getElementById('carrinho-total-valor');
    const checkoutBtn = document.getElementById('checkout-btn');

    function atualizarCarrinho() {
        localStorage.setItem('carrinho', JSON.stringify(carrinho));
        if (contadorCarrinho) {
            contadorCarrinho.textContent = carrinho.length;
        }

        if (carrinhoItensContainer) {
            carrinhoItensContainer.innerHTML = '';
            let total = 0;
            if (carrinho.length === 0) {
                carrinhoItensContainer.innerHTML = '<p>Seu carrinho está vazio.</p>';
                if (checkoutBtn) {
                    checkoutBtn.disabled = true;
                    checkoutBtn.style.backgroundColor = '#ccc';
                    checkoutBtn.style.cursor = 'not-allowed';
                }
            } else {
                if (checkoutBtn) {
                    checkoutBtn.disabled = false;
                    checkoutBtn.style.backgroundColor = '#d32f2f';
                    checkoutBtn.style.cursor = 'pointer';
                }
                carrinho.forEach(item => {
                    const itemElement = document.createElement('div');
                    itemElement.classList.add('carrinho-item');
                    itemElement.innerHTML = `
                        <span>${item.nome}</span>
                        <span>R$ ${item.preco.toFixed(2)}</span>
                    `;
                    carrinhoItensContainer.appendChild(itemElement);
                    total += item.preco;
                });
            }
            carrinhoTotalValor.textContent = total.toFixed(2);
        }
    }

    // Adiciona produtos ao carrinho
    document.querySelectorAll('.add-carrinho-btn').forEach(button => {
        button.addEventListener('click', () => {
            const produto = {
                id: button.dataset.id,
                nome: button.dataset.nome,
                preco: parseFloat(button.dataset.preco),
                imagem: button.dataset.imagem
            };
            carrinho.push(produto);
            atualizarCarrinho();
            alert(`${produto.nome} foi adicionado ao seu carrinho!`);
        });
    });

    // Evento para o botão de checkout
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            if (carrinho.length === 0) {
                alert('Seu carrinho está vazio. Adicione produtos antes de finalizar a compra.');
                return;
            }
            const total = carrinho.reduce((sum, item) => sum + item.preco, 0);
            window.location.href = `/checkout?total=${total.toFixed(2)}`;
        });
    }

    // Lógica da página de checkout (checkout.html)
    const formCheckout = document.getElementById('form-checkout');
    if (formCheckout) {
        document.getElementById('btn-pix').addEventListener('click', () => {
            if (!formCheckout.checkValidity()) {
                alert('Por favor, preencha todos os campos obrigatórios de entrega antes de continuar.');
                return;
            }
            document.getElementById('area-pagamento').style.display = 'block';
            document.getElementById('pix-area').style.display = 'block';
            document.getElementById('cartao-area').style.display = 'none';

            const total = parseFloat(document.getElementById('total-valor').textContent.replace('R$ ', ''));
            fetch('/gerar_pix', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ total: total })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    document.getElementById('qr-code-img').src = `data:image/png;base64,${data.qr_code}`;
                }
            });
        });

        document.getElementById('btn-cartao').addEventListener('click', () => {
            if (!formCheckout.checkValidity()) {
                alert('Por favor, preencha todos os campos obrigatórios de entrega antes de continuar.');
                return;
            }
            document.getElementById('area-pagamento').style.display = 'block';
            document.getElementById('cartao-area').style.display = 'block';
            document.getElementById('pix-area').style.display = 'none';
        });

        document.getElementById('btn-finalizar-pix').addEventListener('click', () => {
            finalizarPagamento('Pix');
        });

        document.getElementById('form-cartao').addEventListener('submit', (e) => {
            e.preventDefault();
            finalizarPagamento('Cartão de Crédito');
        });

        function finalizarPagamento(metodo) {
            const endereco = document.getElementById('endereco').value;
            const cpf = document.getElementById('cpf').value;
            
            fetch('/processar_pagamento', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    carrinho: { itens: carrinho },
                    endereco: endereco,
                    cpf: cpf,
                    metodo_pagamento: metodo
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    alert('Compra finalizada com sucesso! Seus dados foram salvos.');
                    carrinho = [];
                    localStorage.setItem('carrinho', JSON.stringify(carrinho));
                    window.location.href = '/';
                }
            });
        }
    }

    atualizarCarrinho();
});