import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/App";
import { toast } from "sonner";
import { Eye, EyeOff, Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const LOGO_URL = "https://customer-assets.emergentagent.com/job_construction-hub-119/artifacts/t5nlg1av_logo_jose_firmino_word-removebg-preview.png";

export default function Login() {
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "dark");
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const isDark = theme === "dark";

  const [loginData, setLoginData] = useState({ email: "", password: "" });
  const [registerData, setRegisterData] = useState({ name: "", email: "", password: "" });

  useEffect(() => {
    localStorage.setItem("theme", theme);
    document.documentElement.classList.remove("light", "dark");
    document.documentElement.classList.add(theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === "dark" ? "light" : "dark");

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await login(loginData.email, loginData.password);
      toast.success("Sessão iniciada com sucesso!");
      navigate("/");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Erro ao iniciar sessão");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await register(registerData.name, registerData.email, registerData.password);
      toast.success("Conta criada com sucesso!");
      navigate("/");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Erro ao criar conta");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center p-4 ${isDark ? 'bg-neutral-950' : 'bg-gray-100'}`}>
      {/* Theme Toggle */}
      <button
        onClick={toggleTheme}
        className={`fixed top-4 right-4 p-2 rounded-lg transition-colors ${isDark ? 'hover:bg-neutral-800 text-neutral-400 hover:text-white' : 'hover:bg-white text-gray-500 hover:text-gray-900 shadow-sm'}`}
        title={isDark ? "Mudar para modo claro" : "Mudar para modo escuro"}
      >
        {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
      </button>

      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <img 
              src={LOGO_URL} 
              alt="José Firmino" 
              className={`h-16 w-auto object-contain ${!isDark ? 'brightness-0' : ''}`}
              onError={(e) => { e.target.style.display = 'none'; }}
            />
          </div>
          <p className={isDark ? 'text-neutral-400' : 'text-gray-500'}>Gestão de Armazém de Construção Civil</p>
        </div>

        <Card className={isDark ? 'bg-neutral-900 border-neutral-800' : 'bg-white border-gray-200 shadow-lg'}>
          <Tabs defaultValue="login" className="w-full">
            <CardHeader className="pb-0">
              <TabsList className={`grid w-full grid-cols-2 ${isDark ? 'bg-neutral-800' : 'bg-gray-100'}`}>
                <TabsTrigger value="login" data-testid="login-tab" className="data-[state=active]:bg-orange-500 data-[state=active]:text-black">Entrar</TabsTrigger>
                <TabsTrigger value="register" data-testid="register-tab" className="data-[state=active]:bg-orange-500 data-[state=active]:text-black">Registar</TabsTrigger>
              </TabsList>
            </CardHeader>

            <CardContent className="pt-6">
              <TabsContent value="login" className="mt-0">
                <form onSubmit={handleLogin} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="login-email" className={isDark ? 'text-neutral-300' : 'text-gray-700'}>Email</Label>
                    <Input
                      id="login-email"
                      type="email"
                      placeholder="seu@email.com"
                      value={loginData.email}
                      onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
                      required
                      data-testid="login-email-input"
                      className={isDark ? 'bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500' : 'bg-white border-gray-300 placeholder:text-gray-400'}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="login-password" className={isDark ? 'text-neutral-300' : 'text-gray-700'}>Palavra-passe</Label>
                    <div className="relative">
                      <Input
                        id="login-password"
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={loginData.password}
                        onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                        required
                        data-testid="login-password-input"
                        className={`pr-10 ${isDark ? 'bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500' : 'bg-white border-gray-300 placeholder:text-gray-400'}`}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className={`absolute right-3 top-1/2 -translate-y-1/2 ${isDark ? 'text-neutral-500 hover:text-neutral-300' : 'text-gray-400 hover:text-gray-600'}`}
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    </div>
                  </div>
                  <Button
                    type="submit"
                    className="w-full bg-orange-500 hover:bg-orange-600 text-black font-semibold"
                    disabled={isLoading}
                    data-testid="login-submit-btn"
                  >
                    {isLoading ? "A entrar..." : "Entrar"}
                  </Button>
                </form>
              </TabsContent>

              <TabsContent value="register" className="mt-0">
                <form onSubmit={handleRegister} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="register-name" className={isDark ? 'text-neutral-300' : 'text-gray-700'}>Nome</Label>
                    <Input
                      id="register-name"
                      type="text"
                      placeholder="O seu nome"
                      value={registerData.name}
                      onChange={(e) => setRegisterData({ ...registerData, name: e.target.value })}
                      required
                      data-testid="register-name-input"
                      className={isDark ? 'bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500' : 'bg-white border-gray-300 placeholder:text-gray-400'}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="register-email" className={isDark ? 'text-neutral-300' : 'text-gray-700'}>Email</Label>
                    <Input
                      id="register-email"
                      type="email"
                      placeholder="seu@email.com"
                      value={registerData.email}
                      onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })}
                      required
                      data-testid="register-email-input"
                      className={isDark ? 'bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500' : 'bg-white border-gray-300 placeholder:text-gray-400'}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="register-password" className={isDark ? 'text-neutral-300' : 'text-gray-700'}>Palavra-passe</Label>
                    <div className="relative">
                      <Input
                        id="register-password"
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={registerData.password}
                        onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
                        required
                        minLength={6}
                        data-testid="register-password-input"
                        className={`pr-10 ${isDark ? 'bg-neutral-800 border-neutral-700 text-white placeholder:text-neutral-500' : 'bg-white border-gray-300 placeholder:text-gray-400'}`}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className={`absolute right-3 top-1/2 -translate-y-1/2 ${isDark ? 'text-neutral-500 hover:text-neutral-300' : 'text-gray-400 hover:text-gray-600'}`}
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    </div>
                  </div>
                  <Button
                    type="submit"
                    className="w-full bg-orange-500 hover:bg-orange-600 text-black font-semibold"
                    disabled={isLoading}
                    data-testid="register-submit-btn"
                  >
                    {isLoading ? "A criar conta..." : "Criar Conta"}
                  </Button>
                </form>
              </TabsContent>
            </CardContent>
          </Tabs>
        </Card>
      </div>
    </div>
  );
}
