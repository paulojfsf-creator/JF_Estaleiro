import { useState, useRef } from "react";
import { useAuth, API } from "@/App";
import axios from "axios";
import { toast } from "sonner";
import { Upload, FileText, X, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function PdfUpload({ value, onChange, label = "Carregar PDF", isDark = true }) {
  const { token } = useAuth();
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      toast.error("Apenas ficheiros PDF são permitidos");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      toast.error("Ficheiro demasiado grande (máx. 10MB)");
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API}/upload/pdf`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
      onChange(response.data.url);
      toast.success("PDF carregado com sucesso");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Erro ao carregar PDF");
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleRemove = () => {
    onChange("");
  };

  const getFullUrl = (url) => {
    if (!url) return "";
    if (url.startsWith("http")) return url;
    if (url.startsWith("/api")) return `${process.env.REACT_APP_BACKEND_URL}${url}`;
    return url;
  };

  return (
    <div className="space-y-2">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept=".pdf,application/pdf"
        className="hidden"
      />

      {value ? (
        <div className={`flex items-center gap-3 p-3 rounded-lg border ${isDark ? 'bg-neutral-700/50 border-neutral-600' : 'bg-gray-50 border-gray-200'}`}>
          <FileText className="h-5 w-5 text-red-500 flex-shrink-0" />
          <a 
            href={getFullUrl(value)} 
            target="_blank" 
            rel="noopener noreferrer"
            className={`flex-1 text-sm truncate hover:underline ${isDark ? 'text-neutral-200' : 'text-gray-700'}`}
          >
            {value.split("/").pop()}
          </a>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={handleRemove}
            className="text-red-500 hover:text-red-400 hover:bg-red-500/10 h-8 w-8 p-0"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      ) : (
        <Button
          type="button"
          variant="outline"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className={`w-full justify-start ${isDark ? 'border-neutral-600 text-neutral-300 hover:bg-neutral-700' : 'border-gray-300 text-gray-600 hover:bg-gray-50'}`}
        >
          {uploading ? (
            <>
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              A carregar...
            </>
          ) : (
            <>
              <Upload className="h-4 w-4 mr-2" />
              {label}
            </>
          )}
        </Button>
      )}
    </div>
  );
}
