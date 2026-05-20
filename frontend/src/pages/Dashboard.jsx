import Sidebar from '../components/Sidebar'
import Header from '../components/Header'
import DashboardCards from '../components/DashboardCards'
import Grafico from '../components/Grafico'
import TabelaProdutos from '../components/TabelaProdutos'
import Alertas from '../components/Alertas'

function Dashboard() {

    return (

        <div className="app-container">

            <Sidebar />

            <div className="main">

                <Header />

                <div className="page-padding">

                    <DashboardCards />

                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: '2fr 1fr',
                        gap: '20px',
                        marginTop: '20px'
                    }}>

                        <Grafico />

                        <Alertas />

                    </div>

                    <div style={{
                        marginTop: '20px'
                    }}>

                        <TabelaProdutos />

                    </div>

                </div>

            </div>

        </div>
    )
}

export default Dashboard