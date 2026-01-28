import { useState, useRef } from "react";
import { useAuth, API } from "@/App";
import axios from "axios";
import { toast } from "sonner";
import { Upload, X, Image as ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ImageUpload({ value, onChange, label = "Foto" }) {
  const { token } = useAuth();
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState(value || "");
  const fileInputRef = useRef(null);

  const handleFileSelect = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Check file type
    if (!file.type.startsWith("image/")) {
      toast.error("Apenas ficheiros de imagem são permitidos");
      return;
    }

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error("Ficheiro demasiado grande (máx. 5MB)");
      return;
    }

    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(`${API}/upload`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data"
        }
      });

      const imageUrl = `${process.env.REACT_APP_BACKEND_URL}${response.data.url}`;
      setPreview(imageUrl);
      onChange(imageUrl);
      toast.success("Imagem carregada com sucesso");
    } catch (error) {
      toast.error("Erro ao carregar imagem");
      console.error("Upload error:", error);
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = () => {
    setPreview("");
    onChange("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">{label}</label>
      
      <div className="flex items-start gap-4">
        {/* Preview */}
        <div className="relative w-24 h-24 border border-slate-200 rounded-sm overflow-hidden bg-slate-50 flex items-center justify-center">
          {preview ? (
            <>
              <img
                src={preview}
                alt="Preview"
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }}
              />
              <div className="hidden w-full h-full items-center justify-center text-slate-400">
                <ImageIcon className="h-8 w-8" />
              </div>
              <button
                type="button"
                onClick={handleRemove}
                className="absolute top-1 right-1 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
              >
                <X className="h-3 w-3" />
              </button>
            </>
          ) : (
            <ImageIcon className="h-8 w-8 text-slate-300" />
          )}
        </div>

        {/* Upload button */}
        <div className="flex flex-col gap-2">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
            id="image-upload"
          />
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            className="rounded-sm"
          >
            <Upload className="h-4 w-4 mr-2" />
            {uploading ? "A carregar..." : "Carregar Imagem"}
          </Button>
          <p className="text-xs text-slate-500">
            JPG, PNG ou GIF (máx. 5MB)
          </p>
        </div>
      </div>
    </div>
  );
}
