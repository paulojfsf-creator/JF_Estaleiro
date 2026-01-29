import { useState, useEffect } from "react";
import { useAuth, API } from "@/App";
import { Link } from "react-router-dom";
import axios from "axios";
import { toast } from "sonner";
import { Plus, Pencil, Trash2, Wrench, Search, Eye, Building2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Switch } from "@/components/ui/switch";
import ImageUpload from "@/components/ImageUpload";

const estadoOptions = ["Bom", "Razoável", "Mau"];

export default function Equipamentos() {
  const { token } = useAuth();
  const [equipamentos, setEquipamentos] = useState([]);
  const [obras, setObras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [formData, setFormData] = useState({
    codigo: "",
    descricao: "",
    marca: "",
    modelo: "",
    data_aquisicao: "",
    ativo: true,
    categoria: "",
    numero_serie: "",
    estado_conservacao: "Bom",
    foto: "",
    obra_id: ""
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [eqRes, obrasRes] = await Promise.all([
        axios.get(`${API}/equipamentos`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API}/obras`, { headers: { Authorization: `Bearer ${token}` } })
      ]);
      setEquipamentos(eqRes.data);
      setObras(obrasRes.data);
    } catch (error) {
      toast.error("Erro ao carregar dados");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...formData, obra_id: formData.obra_id || null };
      if (selectedItem) {
        await axios.put(`${API}/equipamentos/${selectedItem.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success("Equipamento atualizado");
      } else {
        await axios.post(`${API}/equipamentos`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success("Equipamento criado");
      }
      setDialogOpen(false);
      resetForm();
      fetchData();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Erro ao guardar");
    }
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`${API}/equipamentos/${selectedItem.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success("Equipamento eliminado");
      setDeleteDialogOpen(false);
      setSelectedItem(null);
      fetchData();
    } catch (error) {
      toast.error("Erro ao eliminar");
    }
  };

  const openEditDialog = (item) => {
    setSelectedItem(item);
    setFormData({
      codigo: item.codigo,
      descricao: item.descricao,
      marca: item.marca || "",
      modelo: item.modelo || "",
      data_aquisicao: item.data_aquisicao?.split("T")[0] || "",
      ativo: item.ativo ?? true,
      categoria: item.categoria || "",
      numero_serie: item.numero_serie || "",
      estado_conservacao: item.estado_conservacao || "Bom",
      foto: item.foto || "",
      obra_id: item.obra_id || ""
    });
    setDialogOpen(true);
  };

  const resetForm = () => {
    setSelectedItem(null);
    setFormData({
      codigo: "", descricao: "", marca: "", modelo: "", data_aquisicao: "",
      ativo: true, categoria: "", numero_serie: "",
      estado_conservacao: "Bom", foto: "", obra_id: ""
    });
  };

  const filtered = equipamentos.filter(e => 
    e.codigo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.descricao?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.marca?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getObraName = (obraId) => {
    const obra = obras.find(o => o.id === obraId);
    return obra ? obra.nome : null;
  };

  if (loading) return <div className="flex items-center justify-center h-64"><div className="text-neutral-400">A carregar...</div></div>;

  return (
    <div data-testid="equipamentos-page">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Wrench className="h-7 w-7 text-orange-500" />
            Equipamentos
          </h1>
          <p className="text-neutral-400 text-sm mt-1">Gestão de equipamentos do armazém</p>
        </div>
        <Button onClick={() => { resetForm(); setDialogOpen(true); }} className="bg-orange-500 hover:bg-orange-600 text-black font-semibold" data-testid="add-equipamento-btn">
          <Plus className="h-4 w-4 mr-2" /> Novo Equipamento
        </Button>
      </div>

      {/* Search */}
      <div className="mb-6 relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-neutral-500" />
        <Input
          placeholder="Pesquisar por código, descrição ou marca..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10 bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500"
          data-testid="search-input"
        />
      </div>

      {filtered.length === 0 ? (
        <div className="text-center py-12 bg-neutral-800 border border-neutral-700 rounded-lg">
          <Wrench className="h-12 w-12 text-neutral-600 mx-auto mb-4" />
          <p className="text-neutral-400">{searchTerm ? "Nenhum resultado encontrado" : "Nenhum equipamento registado"}</p>
        </div>
      ) : (
        <div className="overflow-x-auto bg-neutral-800 border border-neutral-700 rounded-lg">
          <table className="w-full" data-testid="equipamentos-table">
            <thead>
              <tr className="border-b border-neutral-700">
                <th className="text-left py-3 px-4 text-neutral-400 font-medium text-sm">Código</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium text-sm">Descrição</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium text-sm">Marca/Modelo</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium text-sm">Estado</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium text-sm">Obra</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium text-sm">Ativo</th>
                <th className="text-right py-3 px-4 text-neutral-400 font-medium text-sm">Ações</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((item) => (
                <tr key={item.id} className="border-b border-neutral-700/50 hover:bg-neutral-700/30" data-testid={`equipamento-row-${item.id}`}>
                  <td className="py-3 px-4 font-mono text-sm text-orange-400">{item.codigo}</td>
                  <td className="py-3 px-4 text-white">{item.descricao}</td>
                  <td className="py-3 px-4 text-neutral-400">{item.marca} {item.modelo}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${item.estado_conservacao === "Bom" ? "bg-emerald-500/20 text-emerald-400" : item.estado_conservacao === "Razoável" ? "bg-amber-500/20 text-amber-400" : "bg-red-500/20 text-red-400"}`}>
                      {item.estado_conservacao}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    {item.obra_id ? (
                      <span className="flex items-center gap-1 text-orange-400 text-sm">
                        <Building2 className="h-3 w-3" />
                        {getObraName(item.obra_id)}
                      </span>
                    ) : (
                      <span className="text-neutral-500 text-sm">Em armazém</span>
                    )}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`h-2 w-2 rounded-full inline-block ${item.ativo ? "bg-emerald-500" : "bg-neutral-500"}`} />
                  </td>
                  <td className="py-3 px-4 text-right">
                    <Link to={`/equipamentos/${item.id}`}>
                      <Button variant="ghost" size="sm" className="text-neutral-400 hover:text-white" data-testid={`view-${item.id}`}>
                        <Eye className="h-4 w-4" />
                      </Button>
                    </Link>
                    <Button variant="ghost" size="sm" onClick={() => openEditDialog(item)} className="text-neutral-400 hover:text-white" data-testid={`edit-${item.id}`}>
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => { setSelectedItem(item); setDeleteDialogOpen(true); }} className="text-red-400 hover:text-red-300" data-testid={`delete-${item.id}`}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Form Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto bg-neutral-900 border-neutral-700">
          <DialogHeader>
            <DialogTitle className="text-white">{selectedItem ? "Editar Equipamento" : "Novo Equipamento"}</DialogTitle>
            <DialogDescription className="text-neutral-400">Preencha os dados do equipamento</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
              <div className="space-y-2">
                <Label className="text-neutral-300">Código *</Label>
                <Input value={formData.codigo} onChange={(e) => setFormData({...formData, codigo: e.target.value})} required data-testid="codigo-input" className="bg-neutral-800 border-neutral-700 text-white" />
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Descrição *</Label>
                <Input value={formData.descricao} onChange={(e) => setFormData({...formData, descricao: e.target.value})} required data-testid="descricao-input" className="bg-neutral-800 border-neutral-700 text-white" />
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Marca</Label>
                <Input value={formData.marca} onChange={(e) => setFormData({...formData, marca: e.target.value})} data-testid="marca-input" className="bg-neutral-800 border-neutral-700 text-white" />
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Modelo</Label>
                <Input value={formData.modelo} onChange={(e) => setFormData({...formData, modelo: e.target.value})} data-testid="modelo-input" className="bg-neutral-800 border-neutral-700 text-white" />
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Categoria</Label>
                <Input value={formData.categoria} onChange={(e) => setFormData({...formData, categoria: e.target.value})} placeholder="Ex: Aparafusadora, Aspirador" data-testid="categoria-input" className="bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500" />
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Nº Série</Label>
                <Input value={formData.numero_serie} onChange={(e) => setFormData({...formData, numero_serie: e.target.value})} data-testid="serie-input" className="bg-neutral-800 border-neutral-700 text-white" />
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Data Aquisição</Label>
                <Input type="date" value={formData.data_aquisicao} onChange={(e) => setFormData({...formData, data_aquisicao: e.target.value})} data-testid="data-input" className="bg-neutral-800 border-neutral-700 text-white" />
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Estado Conservação</Label>
                <Select value={formData.estado_conservacao} onValueChange={(v) => setFormData({...formData, estado_conservacao: v})}>
                  <SelectTrigger className="bg-neutral-800 border-neutral-700 text-white" data-testid="estado-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-neutral-800 border-neutral-700">
                    {estadoOptions.map(e => <SelectItem key={e} value={e} className="text-white hover:bg-neutral-700">{e}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">Obra</Label>
                <Select value={formData.obra_id || "none"} onValueChange={(v) => setFormData({...formData, obra_id: v === "none" ? "" : v})}>
                  <SelectTrigger className="bg-neutral-800 border-neutral-700 text-white" data-testid="obra-select"><SelectValue placeholder="Selecione uma obra" /></SelectTrigger>
                  <SelectContent className="bg-neutral-800 border-neutral-700">
                    <SelectItem value="none" className="text-white hover:bg-neutral-700">Em armazém</SelectItem>
                    {obras.filter(o => o.estado === "Ativa").map(o => <SelectItem key={o.id} value={o.id} className="text-white hover:bg-neutral-700">{o.codigo} - {o.nome}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label className="text-neutral-300">URL Foto</Label>
                <Input value={formData.foto} onChange={(e) => setFormData({...formData, foto: e.target.value})} placeholder="https://..." data-testid="foto-input" className="bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500" />
              </div>
              <div className="md:col-span-2">
                <ImageUpload 
                  value={formData.foto} 
                  onChange={(url) => setFormData({...formData, foto: url})}
                  label="Ou carregar foto"
                />
              </div>
              <div className="flex items-center gap-3">
                <Switch checked={formData.ativo} onCheckedChange={(v) => setFormData({...formData, ativo: v})} data-testid="ativo-switch" />
                <Label className="text-neutral-300">Ativo</Label>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)} className="border-neutral-600 text-neutral-300 hover:bg-neutral-800">Cancelar</Button>
              <Button type="submit" className="bg-orange-500 hover:bg-orange-600 text-black font-semibold" data-testid="submit-btn">{selectedItem ? "Guardar" : "Criar"}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent className="bg-neutral-900 border-neutral-700">
          <AlertDialogHeader>
            <AlertDialogTitle className="text-white">Eliminar Equipamento</AlertDialogTitle>
            <AlertDialogDescription className="text-neutral-400">Tem a certeza que deseja eliminar "{selectedItem?.descricao}"?</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel className="border-neutral-600 text-neutral-300 hover:bg-neutral-800">Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-red-500 hover:bg-red-600 text-white" data-testid="confirm-delete-btn">Eliminar</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
