/**
 * ═══════════════════════════════════════════════════════════════════════════
 *              P5.JS ARTE GENERATIVO - BUENAS PRÁCTICAS
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * Este archivo muestra ESTRUCTURA y PRINCIPIOS para arte generativo con p5.js.
 * NO prescribe qué arte debes crear.
 *
 * Tu filosofía algorítmica debe guiar lo que construyes.
 * Esto son solo buenas prácticas de cómo estructurar el código.
 *
 * ═══════════════════════════════════════════════════════════════════════════
 */

// ============================================================================
// 1. ORGANIZACIÓN DE PARÁMETROS
// ============================================================================
// Guarda todos los parámetros ajustables en un solo objeto.
// Esto facilita:
// - Conectarlos a controles de UI
// - Restaurar valores por defecto
// - Serializar/guardar configuraciones

let params = {
    // Define los parámetros que correspondan a TU algoritmo
    // Ejemplos (personaliza para tu pieza):
    // - Cantidades: cuántos elementos (partículas, círculos, ramas, etc.)
    // - Escalas: tamaño, velocidad, espaciado
    // - Probabilidades: qué tan seguido ocurre un evento
    // - Ángulos: rotación, dirección
    // - Colores: arreglos de paleta

    seed: 12345,
    // define colorPalette como un arreglo -- elige los colores que quieras ['#e8b84b', '#f7e3a1', '#b8860b', '#b0aea5']
    // Agrega TUS parámetros aquí según tu algoritmo
};

// ============================================================================
// 2. ALEATORIEDAD CON SEMILLA (crítico para la reproducibilidad)
// ============================================================================
// SIEMPRE usa aleatoriedad con semilla para salida reproducible estilo Art Blocks

function initializeSeed(seed) {
    randomSeed(seed);
    noiseSeed(seed);
    // A partir de aquí, todas las llamadas a random() y noise() son deterministas
}

// ============================================================================
// 3. CICLO DE VIDA DE P5.JS
// ============================================================================

function setup() {
    createCanvas(800, 800);

    // Inicializa la semilla primero
    initializeSeed(params.seed);

    // Configura tu sistema generativo aquí.
    // Es donde inicializas:
    // - Arreglos de objetos
    // - Estructuras de grilla
    // - Posiciones iniciales
    // - Estados de partida

    // Para arte estático: llama noLoop() al final de setup()
    // Para arte animado: deja que draw() siga corriendo
}

function draw() {
    // Opción 1: Generación estática (corre una vez y se detiene)
    // - Genera todo en setup()
    // - Llama noLoop() en setup()
    // - draw() casi no hace nada o puede quedar vacío

    // Opción 2: Generación animada (continua)
    // - Actualiza tu sistema en cada frame
    // - Patrones comunes: movimiento de partículas, crecimiento, evolución
    // - Opcionalmente llama noLoop() después de N frames

    // Opción 3: Regeneración disparada por el usuario
    // - Usa noLoop() por defecto
    // - Llama redraw() cuando cambien los parámetros
}

// ============================================================================
// 4. ESTRUCTURA DE CLASES (cuando necesitas objetos)
// ============================================================================
// Usa clases cuando tu algoritmo involucra múltiples entidades.
// Ejemplos: partículas, agentes, células, nodos, etc.

class Entity {
    constructor() {
        // Inicializa las propiedades de la entidad
        // Usa random() aquí — ya va con la semilla puesta
    }

    update() {
        // Actualiza el estado de la entidad
        // Esto puede incluir:
        // - Cálculos de física
        // - Reglas de comportamiento
        // - Interacciones con vecinos
    }

    display() {
        // Dibuja la entidad
        // Mantén la lógica de render separada de la de actualización
    }
}

// ============================================================================
// 5. CONSIDERACIONES DE RENDIMIENTO
// ============================================================================

// Para grandes cantidades de elementos:
// - Precalcula todo lo que puedas
// - Usa detección de colisión simple (spatial hashing si hace falta)
// - Limita operaciones costosas (sqrt, trig) cuando sea posible
// - Usa los vectores de p5 de forma eficiente

// Para animación fluida:
// - Apunta a 60fps
// - Perfila si algo va lento
// - Considera reducir el número de partículas o simplificar cálculos

// ============================================================================
// 6. FUNCIONES UTILITARIAS
// ============================================================================

// Utilidades de color
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function colorFromPalette(index) {
    return params.colorPalette[index % params.colorPalette.length];
}

// Mapeo y easing
function mapRange(value, inMin, inMax, outMin, outMax) {
    return outMin + (outMax - outMin) * ((value - inMin) / (inMax - inMin));
}

function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// Restringir a un rango
function wrapAround(value, max) {
    if (value < 0) return max;
    if (value > max) return 0;
    return value;
}

// ============================================================================
// 7. ACTUALIZACIÓN DE PARÁMETROS (conectar a la UI)
// ============================================================================

function updateParameter(paramName, value) {
    params[paramName] = value;
    // Decide si hace falta regenerar o solo actualizar
    // Algunos parámetros se actualizan en vivo, otros necesitan regenerar todo
}

function regenerate() {
    // Reinicializa tu sistema generativo
    // Útil cuando los parámetros cambian de forma significativa
    initializeSeed(params.seed);
    // Luego regenera tu sistema
}

// ============================================================================
// 8. PATRONES COMUNES DE P5.JS
// ============================================================================

// Dibujar con transparencia para estelas/desvanecidos
function fadeBackground(opacity) {
    fill(250, 249, 245, opacity); // Golden light con alpha
    noStroke();
    rect(0, 0, width, height);
}

// Usar ruido para variación orgánica
function getNoiseValue(x, y, scale = 0.01) {
    return noise(x * scale, y * scale);
}

// Crear vectores a partir de ángulos
function vectorFromAngle(angle, magnitude = 1) {
    return createVector(cos(angle), sin(angle)).mult(magnitude);
}

// ============================================================================
// 9. FUNCIONES DE EXPORTACIÓN
// ============================================================================

function exportImage() {
    saveCanvas('generative-art-' + params.seed, 'png');
}

// ============================================================================
// RECORDATORIO
// ============================================================================
//
// Esto son HERRAMIENTAS y PRINCIPIOS, no una receta.
// Tu filosofía algorítmica debe guiar QUÉ creas.
// Esta estructura te ayuda a crearlo BIEN.
//
// Enfócate en:
// - Código limpio y legible
// - Parametrizado para explorar variaciones
// - Con semilla para reproducibilidad
// - Ejecución performante
//
// El arte en sí depende enteramente de ti!
//
// ============================================================================
