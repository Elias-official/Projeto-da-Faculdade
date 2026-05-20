const form = document.getElementById('formProduto');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const produto = {
        nome: document.getElementById('nome').value,
        categoria: document.getElementById('categoria').value,
        estoque_minimo: document.getElementById('estoque_minimo').value,
        preco: parseFloat(document.getElementById('preco').value),
        quantidade: parseInt(document.getElementById('quantidade').value)
    };

    const resposta = await fetch('/produtos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(produto)
    });

    const dados = await resposta.json();

    alert(dados.mensagem);

    carregarProdutos();
});

let produtos = [];

async function carregarProdutos() {

    const res = await fetch('/produtos');

    produtos = await res.json();

    const datalist = document.getElementById('produtos');

    datalist.innerHTML = '';

    produtos.forEach(p => {

        datalist.innerHTML += `
            <option value="${p.nome}">
        `;
    });

    console.log(produtos);

}