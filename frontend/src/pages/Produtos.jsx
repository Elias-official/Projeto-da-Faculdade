import { useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'
import Sidebar from '../components/Sidebar'
import Header from '../components/Header'
import TabelaProdutos from '../components/TabelaProdutos'
import ProdutoModal from '../components/ProdutoModal'

function Produtos() {
  const [produtos, setProdutos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [filtro, setFiltro] = useState({ search: '', categoria: '', status: '' })
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [produtoSelecionado, setProdutoSelecionado] = useState(null)

  useEffect(() => {
    buscarCategorias()
  }, [])

  useEffect(() => {
    buscarProdutos()
  }, [filtro])

  async function buscarCategorias() {
    try {
      const response = await api.get('/categorias')
      setCategorias(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  async function buscarProdutos() {
    setLoading(true)
    try {
      const response = await api.get('/produtos', { params: filtro })
      setProdutos(response.data)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const produtosVisiveis = useMemo(
    () => produtos.filter((item) => {
      if (!filtro.status) return true
      return item.status.toLowerCase().includes(filtro.status.toLowerCase())
    }),
    [produtos, filtro.status]
  )

  function abrirModal(produto = null) {
    setProdutoSelecionado(produto)
    setModalOpen(true)
  }

  async function salvarProduto(dados) {
    try {
      if (dados.id) {
        await api.put(`/produtos/${dados.id}`, dados)
      } else {
        await api.post('/produtos', dados)
      }
      setModalOpen(false)
      buscarProdutos()
    } catch (error) {
      console.error(error)
      alert('Erro ao salvar produto')
    }
  }

  async function excluirProduto(id) {
    if (!confirm('Deseja remover este produto?')) {
      return
    }
    try {
      await api.delete(`/produtos/${id}`)
      buscarProdutos()
    } catch (error) {
      console.error(error)
      alert('Erro ao excluir produto')
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-5 lg:p-8">
          <Header />
          <div className="mt-6 space-y-6">
            <div className="glass-card p-6">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <h1 className="text-2xl font-semibold">Gerenciar Produtos</h1>
                  <p className="mt-1 text-slate-400">Busca, filtros e estoque inteligente em tempo real.</p>
                </div>
                <button
                  className="inline-flex items-center justify-center rounded-2xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-500"
                  onClick={() => abrirModal()}
                >
                  Adicionar produto
                </button>
              </div>
              <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                <input
                  value={filtro.search}
                  onChange={(e) => setFiltro((prev) => ({ ...prev, search: e.target.value }))}
                  placeholder="Pesquisar código, produto, marca ou categoria"
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 placeholder:text-slate-500 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                />
                <select
                  value={filtro.categoria}
                  onChange={(e) => setFiltro((prev) => ({ ...prev, categoria: e.target.value }))}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                >
                  <option value="">Todas as categorias</option>
                  {categorias.map((categoria) => (
                    <option key={categoria.id} value={categoria.nome}>
                      {categoria.nome}
                    </option>
                  ))}
                </select>
                <select
                  value={filtro.status}
                  onChange={(e) => setFiltro((prev) => ({ ...prev, status: e.target.value }))}
                  className="rounded-3xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-100 shadow-soft focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                >
                  <option value="">Todos os status</option>
                  <option value="Estoque normal">Normal</option>
                  <option value="Atenção: Estoque baixo">Atenção</option>
                  <option value="Crítico: Estoque muito baixo">Crítico</option>
                  <option value="Sem estoque">Sem estoque</option>
                </select>
              </div>
            </div>
            <div className="glass-card p-6">
              <h2 className="text-xl font-semibold">Tabela de produtos</h2>
              <div className="mt-4 overflow-x-auto">
                <TabelaProdutos
                  produtos={produtosVisiveis}
                  loading={loading}
                  onEdit={abrirModal}
                  onDelete={excluirProduto}
                />
              </div>
            </div>
          </div>
        </main>
      </div>
      {modalOpen && (
        <ProdutoModal
          open={modalOpen}
          produto={produtoSelecionado}
          categorias={categorias}
          onClose={() => setModalOpen(false)}
          onSave={salvarProduto}
        />
      )}
    </div>
  )
}

export default Produtos