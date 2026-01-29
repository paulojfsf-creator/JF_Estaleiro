import { useState } from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "@/App";
import {
  LayoutDashboard,
  Wrench,
  Truck,
  Package,
  Building2,
  ArrowLeftRight,
  FileText,
  Menu,
  X,
  LogOut,
  User,
  ChevronLeft,
  ChevronDown,
  Upload,
  Download
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { Button } from "@/components/ui/button";

const LOGO_URL = "https://customer-assets.emergentagent.com/job_construction-hub-119/artifacts/t5nlg1av_logo_jose_firmino_word-removebg-preview.png";

const navItems = [
  { path: "/", icon: LayoutDashboard, label: "Dashboard" },
  { path: "/equipamentos", icon: Wrench, label: "Equipamentos" },
  { path: "/viaturas", icon: Truck, label: "Viaturas" },
  { path: "/materiais", icon: Package, label: "Materiais" },
  { path: "/obras", icon: Building2, label: "Obras" },
];

const movimentosItems = [
  { path: "/movimentos/ativos", label: "Mov. Ativos" },
  { path: "/movimentos/stock", label: "Mov. Stock" },
  { path: "/movimentos/viaturas", label: "Mov. Viaturas" },
];

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [movimentosOpen, setMovimentosOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-neutral-900">
      {mobileOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside 
        className={`fixed left-0 top-0 h-full bg-neutral-950 text-white transition-all duration-300 z-50 overflow-y-auto
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full'} 
          md:translate-x-0 ${sidebarOpen ? 'w-64' : 'w-20'}`}
      >
        <div className="h-20 flex items-center justify-between px-4 border-b border-neutral-800">
          {sidebarOpen && (
            <div className="flex items-center">
              <img 
                src={LOGO_URL} 
                alt="José Firmino" 
                className="h-12 w-auto object-contain"
                onError={(e) => { e.target.style.display = 'none'; }}
              />
            </div>
          )}
          <button
            data-testid="toggle-sidebar-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-neutral-800 rounded-sm hidden md:block"
          >
            <ChevronLeft className={`h-5 w-5 transition-transform ${!sidebarOpen ? 'rotate-180' : ''}`} />
          </button>
          <button
            data-testid="close-mobile-sidebar-btn"
            onClick={() => setMobileOpen(false)}
            className="p-2 hover:bg-neutral-800 rounded-sm md:hidden"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="py-4">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              data-testid={`nav-${item.label.toLowerCase().replace(/\s/g, '-')}`}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) => 
                `flex items-center gap-3 px-4 py-3 text-neutral-400 hover:bg-neutral-800 hover:text-white transition-colors
                ${isActive ? 'bg-neutral-800 text-white border-l-4 border-orange-500' : ''}`
              }
            >
              <item.icon className="h-5 w-5 flex-shrink-0" />
              {sidebarOpen && <span>{item.label}</span>}
            </NavLink>
          ))}
          
          {/* Movimentos Collapsible */}
          <Collapsible open={movimentosOpen} onOpenChange={setMovimentosOpen}>
            <CollapsibleTrigger className="flex items-center gap-3 px-4 py-3 w-full text-neutral-400 hover:bg-neutral-800 hover:text-white transition-colors">
              <ArrowLeftRight className="h-5 w-5 flex-shrink-0" />
              {sidebarOpen && (
                <>
                  <span className="flex-1 text-left">Movimentos</span>
                  <ChevronDown className={`h-4 w-4 transition-transform ${movimentosOpen ? 'rotate-180' : ''}`} />
                </>
              )}
            </CollapsibleTrigger>
            <CollapsibleContent>
              {movimentosItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileOpen(false)}
                  className={({ isActive }) => 
                    `flex items-center gap-3 px-4 py-2 pl-12 text-neutral-500 hover:bg-neutral-800 hover:text-white transition-colors text-sm
                    ${isActive ? 'bg-neutral-800 text-white' : ''}`
                  }
                >
                  {sidebarOpen && <span>{item.label}</span>}
                </NavLink>
              ))}
            </CollapsibleContent>
          </Collapsible>

          <NavLink
            to="/relatorios"
            data-testid="nav-relatorios"
            onClick={() => setMobileOpen(false)}
            className={({ isActive }) => 
              `flex items-center gap-3 px-4 py-3 text-neutral-400 hover:bg-neutral-800 hover:text-white transition-colors
              ${isActive ? 'bg-neutral-800 text-white border-l-4 border-orange-500' : ''}`
            }
          >
            <FileText className="h-5 w-5 flex-shrink-0" />
            {sidebarOpen && <span>Relatórios</span>}
          </NavLink>
        </nav>
      </aside>

      <div className={`transition-all duration-300 ${sidebarOpen ? 'md:ml-64' : 'md:ml-20'}`}>
        <header className="h-16 bg-neutral-950 border-b border-neutral-800 flex items-center justify-between px-4 md:px-6 sticky top-0 z-30">
          <button
            data-testid="open-mobile-sidebar-btn"
            onClick={() => setMobileOpen(true)}
            className="p-2 hover:bg-neutral-800 rounded-sm md:hidden text-white"
          >
            <Menu className="h-5 w-5" />
          </button>

          <div className="flex-1" />

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="flex items-center gap-2 text-neutral-300 hover:text-white hover:bg-neutral-800" data-testid="user-menu-btn">
                <div className="h-8 w-8 bg-orange-500 rounded-full flex items-center justify-center">
                  <User className="h-4 w-4 text-black" />
                </div>
                <span className="hidden md:block text-sm font-medium">{user?.name}</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48 bg-neutral-900 border-neutral-700">
              <DropdownMenuItem onClick={handleLogout} data-testid="logout-btn" className="text-neutral-300 hover:text-white focus:bg-neutral-800">
                <LogOut className="h-4 w-4 mr-2" />
                Terminar Sessão
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </header>

        <main className="p-4 md:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
