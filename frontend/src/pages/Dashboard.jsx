import { useState, useEffect } from "react";
import { useAuth, API } from "@/App";
import axios from "axios";
import { 
  Wrench, 
  Truck, 
  Package, 
  MapPin,
  Building2,
  AlertTriangle,
  CheckCircle,
  XCircle
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Dashboard() {
  const { token } = useAuth();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      const response = await axios.get(`${API}/summary`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSummary(response.data);
    } catch (error) {
      console.error("Error fetching summary:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">A carregar...</div>
      </div>
    );
  }

  return (
    <div data-testid="dashboard-page">
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Visão geral do armazém</p>
      </div>

      {/* Alerts Section */}
      {summary?.alerts && summary.alerts.length > 0 && (
        <div className="mb-8 animate-fade-in">
          <h2 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-500" />
            Alertas ({summary.alerts.length})
          </h2>
          <div className="grid gap-3 max-h-64 overflow-y-auto">
            {summary.alerts.map((alert, idx) => (
              <div 
                key={idx} 
                className={`alert-card ${alert.urgent ? 'urgent' : ''}`}
                data-testid={`alert-${idx}`}
              >
                <AlertTriangle className={`h-5 w-5 flex-shrink-0 ${alert.urgent ? 'text-red-500' : 'text-amber-500'}`} />
                <div>
                  <p className="font-medium text-slate-900">{alert.item}</p>
                  <p className={`text-sm ${alert.urgent ? 'text-red-600' : 'text-amber-600'}`}>
                    {alert.message}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4 mb-8">
        <Card className="stat-card animate-fade-in" data-testid="stat-equipamentos">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Equipamentos
            </CardTitle>
            <Wrench className="h-5 w-5 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-slate-900">{summary?.equipamentos?.total || 0}</div>
            <div className="mt-2 flex gap-3 text-sm">
              <span className="flex items-center gap-1 text-emerald-600">
                <CheckCircle className="h-3.5 w-3.5" /> {summary?.equipamentos?.ativos || 0}
              </span>
              <span className="flex items-center gap-1 text-slate-400">
                <XCircle className="h-3.5 w-3.5" /> {summary?.equipamentos?.inativos || 0}
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="stat-card animate-fade-in stagger-1" data-testid="stat-viaturas">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Viaturas
            </CardTitle>
            <Truck className="h-5 w-5 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-slate-900">{summary?.viaturas?.total || 0}</div>
            <div className="mt-2 flex gap-3 text-sm">
              <span className="flex items-center gap-1 text-emerald-600">
                <CheckCircle className="h-3.5 w-3.5" /> {summary?.viaturas?.ativas || 0}
              </span>
              <span className="flex items-center gap-1 text-slate-400">
                <XCircle className="h-3.5 w-3.5" /> {summary?.viaturas?.inativas || 0}
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="stat-card animate-fade-in stagger-2" data-testid="stat-materiais">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Materiais
            </CardTitle>
            <Package className="h-5 w-5 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-slate-900">{summary?.materiais?.total || 0}</div>
            <p className="text-sm text-slate-500 mt-1">
              Stock total: {summary?.materiais?.stock_total || 0}
            </p>
          </CardContent>
        </Card>

        <Card className="stat-card animate-fade-in stagger-3" data-testid="stat-locais">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Locais
            </CardTitle>
            <MapPin className="h-5 w-5 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-slate-900">{summary?.locais?.total || 0}</div>
            <div className="mt-2 flex gap-2 text-xs">
              <span className="bg-slate-100 px-2 py-0.5 rounded">{summary?.locais?.armazens || 0} Arm.</span>
              <span className="bg-slate-100 px-2 py-0.5 rounded">{summary?.locais?.oficinas || 0} Ofi.</span>
              <span className="bg-slate-100 px-2 py-0.5 rounded">{summary?.locais?.obras || 0} Obr.</span>
            </div>
          </CardContent>
        </Card>

        <Card className="stat-card animate-fade-in stagger-4" data-testid="stat-obras">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Obras
            </CardTitle>
            <Building2 className="h-5 w-5 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-black text-slate-900">{summary?.obras?.total || 0}</div>
            <div className="mt-2 flex gap-2 text-xs">
              <span className="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">{summary?.obras?.ativas || 0} Ativas</span>
              <span className="bg-slate-100 px-2 py-0.5 rounded">{summary?.obras?.concluidas || 0} Conc.</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
