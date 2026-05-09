const form = document.getElementById('formProduto');

form.addEventListener('submit', async (e) => {

    e.preventDefault();
        
    const produto = {
        nome: document.getElementById('nome').value,
        categoria: document.getElementById('categoria').value,
        estoque_minimo: document.getElementById('estoque_minimo').value,
        preco: parseFloat(document.getElementById('preco').value),
        quantidade: parseInt(document.getElementById('quantidade').value)
    }
    const resposta = await fetch('/produtos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(produto)
    });

const dados = await resposta.json()

alert(dados.mesagem);

})
