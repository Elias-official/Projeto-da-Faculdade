import { useEffect, useState } from 'react'

function ProdutoModal({ open, produto, categorias, onClose, onSave }) {
  const [form, setForm] = useState({
    id: null,
    codigo: '',
    produto: '',
    marca: '',
    categoria: '',
    estoque_atual: '',
    estoque_minimo: '',
    preco: '',
  })

  useEffect(() => {
    if (produto) {
      setForm({
        id: produto.id,
        codigo: produto.codigo,
        produto: produto.produto,
        marca: produto.marca,
        categoria: produto.categoria,
        estoque_atual: produto.estoque_atual,
        estoque_minimo: produto.estoque_minimo,
        preco: produto.preco,
      })
    } else {
      setForm({
        id: null,
        codigo: '',
        produto: '',
        marca: '',
        categoria: categorias[0]?.nome || '',
        estoque_atual: '',
        estoque_minimo: '',
        preco: '',
      })
    }
  }, [produto, categorias])

  if (!open) {
    return null
  }

  function handleChange(event) {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  function submit(event) {
    event.preventDefault()
    onSave({
      ...form,
      estoque_atual: Number(form.estoque_atual),
      estoque_minimo: Number(form.estoque_minimo),
      preco: Number(form.preco),
    })
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4 py-6 backdrop-blur-sm">
      <div className="w-full max-w-3xl rounded-[2rem] border border-slate-800 bg-slate-950/95 p-6 shadow-soft">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-semibold text-slate-100">{form.id ? 'Editar produto' : 'Novo produto'}</h2>
            <p className="mt-2 text-sm text-slate-400">Preencha os dados do produto e salve no estoque.</p>
          </div>
          <button onClick={onClose} className="rounded-3xl bg-slate-900 px-4 py-3 text-sm text-slate-200 transition hover:bg-slate-800">
            Fechar
          </button>
        </div>
        <form className="mt-6 grid gap-4 md:grid-cols-2" onSubmit={submit}>
          <input
            name="codigo"
            value={form.codigo}
            onChange={handleChange}
            placeholder="Código"
            className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          />
          <input
            name="produto"
            value={form.produto}
            onChange={handleChange}
            placeholder="Produto"
            className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          />
          <input
            name="marca"
            value={form.marca}
            onChange={handleChange}
            placeholder="Marca"
            className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          />
          <select
            name="categoria"
            value={form.categoria}
            onChange={handleChange}
            className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          >
            {categorias.map((categoria) => (
              <option key={categoria.id} value={categoria.nome}>{categoria.nome}</option>
            ))}
          </select>
          <input
            name="estoque_atual"
            type="number"
            value={form.estoque_atual}
            onChange={handleChange}
            placeholder="Estoque atual"
            className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          />
          <input
            name="estoque_minimo"
            type="number"
            value={form.estoque_minimo}
            onChange={handleChange}
            placeholder="Estoque mínimo"
            className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          />
          <input
            name="preco"
            type="number"
            step="0.01"
            value={form.preco}
            onChange={handleChange}
            placeholder="Preço"
            className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
          />
          <button className="col-span-full rounded-3xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-500">
            Salvar produto
          </button>
        </form>
      </div>
    </div>
  )
}

export default ProdutoModal
