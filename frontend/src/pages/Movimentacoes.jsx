import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Sidebar from '../components/Sidebar'
import Header from '../components/Header'

function Movimentacoes() {
  const [movimentacoes, setMovimentacoes] = useState([])
  const [produtos, setProdutos] = useState([])
  const [form, setForm] = useState({ produto_id: '', tipo: 'Entrada', quantidade: '' })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    buscarProdutos()
    buscarMovimentacoes()
  }, [])

  async function buscarProdutos() {
    try {
      const response = await api.get('/produtos')
      setProdutos(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  async function buscarMovimentacoes() {
    setLoading(true)
    try {
      const response = await api.get('/movimentacoes')
      setMovimentacoes(response.data)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  async function criarMovimentacao(event) {
    event.preventDefault()
    try {
      await api.post('/movimentacoes', {
        produto_id: Number(form.produto_id),
        tipo: form.tipo,
        quantidade: Number(form.quantidade),
      })
      setForm({ produto_id: '', tipo: 'Entrada', quantidade: '' })
      buscarMovimentacoes()
    } catch (error) {
      console.error(error)
      alert('Erro ao registrar movimentação')
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-5 lg:p-8">
          <Header />
          <div className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
            <section className="glass-card p-6">
              <h1 className="text-2xl font-semibold">Movimentações</h1>
              <p className="mt-2 text-slate-400">Registre entradas e saídas para atualizar o estoque automaticamente.</p>
              <form className="mt-6 space-y-4" onSubmit={criarMovimentacao}>
                <div className="grid gap-4 sm:grid-cols-2">
                  <select
                    className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                    value={form.produto_id}
                    onChange={(e) => setForm((prev) => ({ ...prev, produto_id: e.target.value }))}
                  >
                    <option value="">Produto</option>
                    {produtos.map((produto) => (
                      <option key={produto.id} value={produto.id}>
                        {produto.codigo} - {produto.produto}
                      </option>
                    ))}
                  </select>
                  <select
                    className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                    value={form.tipo}
                    onChange={(e) => setForm((prev) => ({ ...prev, tipo: e.target.value }))}
                  >
                    <option value="Entrada">Entrada</option>
                    <option value="Saída">Saída</option>
                  </select>
                </div>
                <input
                  type="number"
                  value={form.quantidade}
                  onChange={(e) => setForm((prev) => ({ ...prev, quantidade: e.target.value }))}
                  placeholder="Quantidade"
                  className="w-full rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                />
                <button className="w-full rounded-3xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-500">
                  Registrar movimentação
                </button>
              </form>
            </section>
            <section className="glass-card p-6">
              <h2 className="text-xl font-semibold">Últimas movimentações</h2>
              <div className="mt-5 space-y-3">
                {loading ? (
                  <p className="text-slate-400">Carregando histórico...</p>
                ) : movimentacoes.length === 0 ? (
                  <p className="text-slate-400">Nenhuma movimentação registrada ainda.</p>
                ) : (
                  <div className="space-y-3">
                    {movimentacoes.slice(0, 8).map((mov) => (
                      <div key={mov.id} className="rounded-3xl border border-slate-800 bg-slate-950/90 p-4 shadow-soft">
                        <div className="flex items-center justify-between gap-3 text-sm text-slate-300">
                          <span>{mov.produto || 'Produto removido'}</span>
                          <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-200">{mov.tipo}</span>
                        </div>
                        <div className="mt-2 text-sm text-slate-400">
                          <p>Qtd: {mov.quantidade}</p>
                          <p>Usuário: {mov.usuario_id}</p>
                          <p>Data: {new Date(mov.data_movimentacao).toLocaleString('pt-BR')}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Movimentacoes