import { useEffect, useState } from 'react'
import API_URL from '../services/api'

function DashboardCards() {

    const [dados, setDados] = useState({})

    useEffect(() => {

        buscarDashboard()

    }, [])

    async function buscarDashboard() {

        const response = await fetch(`${API_URL}/dashboard`)

        const data = await response.json()

        setDados(data)
    }

    return (

        <div className="cards-grid">

            <div className="card">
                <h3>Total Produtos</h3>
                <h1>{dados.total_produtos ?? 0}</h1>
            </div>
            <div className="card">
                <h3>Itens em Estoque</h3>
                <h1>{dados.estoque_total ?? 0}</h1>
            </div>
            <div className="card">
                <h3>Estoque Baixo</h3>
                <h1>{dados.estoque_baixo ?? 0}</h1>
            </div>
            <div className="card">
                <h3>Valor Estoque</h3>
                <h1>
                    R$ {Number(dados.valor_estoque ?? 0).toLocaleString('pt-BR', {minimumFractionDigits:2, maximumFractionDigits:2})}
                </h1>
            </div>

        </div>
    )
}

const card = {

    background: 'white',

    padding: '20px',

    borderRadius: '12px',

    boxShadow: '0px 2px 5px rgba(0,0,0,0.1)'
}

export default DashboardCards