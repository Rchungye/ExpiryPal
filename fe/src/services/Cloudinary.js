import { cloudinary } from './cloudinary.config';

// Función para subir una imagen
export const subirImagen = async (filePath) => {
  try {
    const result = await cloudinary.uploader.upload(filePath, {
      folder: 'DS56'
    });
    return result;
  } catch (error) {
    throw new Error(`Error subiendo imagen: ${error.message}`);
  }
};

// Función para subir un video
export const subirVideo = async (filePath) => {
  try {
    const result = await cloudinary.uploader.upload(filePath, {
      resource_type: 'video',
      folder: 'DS56'
    });
    return result;
  } catch (error) {
    throw new Error(`Error subiendo video: ${error.message}`);
  }
};

// Función para obtener una lista de recursos (imágenes/videos)
export const obtenerRecursos = async (resourceType = 'image') => {
  try {
    const result = await cloudinary.api.resources({
      resource_type: resourceType,
      type: 'upload',
      prefix: 'DS56/'
    });
    return result.resources;
  } catch (error) {
    throw new Error(`Error obteniendo recursos: ${error.message}`);
  }
};

// Función para actualizar un recurso (cambiar el nombre, mover de carpeta, etc.)
export const actualizarRecurso = async (publicId, options) => {
  try {
    const result = await cloudinary.uploader.rename(publicId, options.new_public_id);
    return result;
  } catch (error) {
    throw new Error(`Error actualizando recurso: ${error.message}`);
  }
};

// Función para eliminar un recurso
export const eliminarRecurso = async (publicId) => {
  try {
    const result = await cloudinary.uploader.destroy(publicId);
    return result;
  } catch (error) {
    throw new Error(`Error eliminando recurso: ${error.message}`);
  }
};
