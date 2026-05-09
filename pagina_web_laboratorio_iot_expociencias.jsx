export default function LaboratorioIoTPage() {
  const stats = [
    { label: 'Nivel de aprobación', value: '90%' },
    { label: 'Comprensión IoT', value: '85%' },
    { label: 'Prácticas completadas', value: '88%' },
    { label: 'Participación activa', value: '95%' },
  ];

  const objetivos = [
    'Fortalecer competencias técnicas y pensamiento lógico.',
    'Promover el aprendizaje práctico mediante IoT y microcontroladores.',
    'Desarrollar habilidades de resolución de problemas en tiempo real.',
    'Impulsar el interés por tecnologías emergentes e inteligencia artificial.',
  ];

  const tecnologias = [
    'ESP32',
    'Sensores y actuadores',
    'Microcontroladores',
    'Internet de las Cosas (IoT)',
    'Automatización',
    'Inteligencia Artificial',
    'Programación',
    'Sistemas embebidos',
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white font-sans">
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-slate-800">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-blue-500/10"></div>

        <div className="relative max-w-7xl mx-auto px-6 py-24 grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <p className="text-cyan-400 font-semibold tracking-widest uppercase mb-4">
              Expo Ciencias Coahuila 2025
            </p>

            <h1 className="text-5xl md:text-6xl font-black leading-tight mb-6">
              Laboratorio IoT de
              <span className="text-cyan-400"> Microcontroladores </span>
              e Inteligencia Artificial
            </h1>

            <p className="text-slate-300 text-lg leading-relaxed mb-8">
              Proyecto educativo orientado a fortalecer el aprendizaje práctico
              en programación, automatización, IoT e inteligencia artificial
              mediante laboratorios accesibles, interactivos y basados en
              tecnologías reales.
            </p>

            <div className="flex flex-wrap gap-4">
              <button className="bg-cyan-500 hover:bg-cyan-400 transition px-6 py-3 rounded-2xl font-semibold text-slate-950 shadow-lg">
                Explorar Proyecto
              </button>

              <button className="border border-slate-700 hover:border-cyan-400 transition px-6 py-3 rounded-2xl font-semibold">
                Ver Resultados
              </button>
            </div>
          </div>

          <div className="relative">
            <div className="bg-slate-900 border border-slate-800 rounded-[2rem] p-8 shadow-2xl backdrop-blur">
              <div className="grid grid-cols-2 gap-5">
                {stats.map((item, index) => (
                  <div
                    key={index}
                    className="bg-slate-800/60 rounded-2xl p-6 border border-slate-700"
                  >
                    <div className="text-4xl font-black text-cyan-400 mb-2">
                      {item.value}
                    </div>
                    <div className="text-slate-300 text-sm">
                      {item.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sobre el proyecto */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-4xl font-bold mb-6">
              ¿Qué es este laboratorio?
            </h2>

            <p className="text-slate-300 leading-relaxed mb-5">
              Este proyecto nace con el objetivo de acercar tecnologías
              emergentes a estudiantes de áreas tecnológicas mediante un entorno
              práctico basado en Internet de las Cosas, automatización e
              inteligencia artificial.
            </p>

            <p className="text-slate-300 leading-relaxed">
              El laboratorio integra sensores, actuadores,
              microcontroladores y plataformas de programación para desarrollar
              competencias técnicas aplicadas a problemas reales.
            </p>
          </div>

          <div className="grid gap-4">
            {objetivos.map((objetivo, index) => (
              <div
                key={index}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex items-start gap-4"
              >
                <div className="w-3 h-3 bg-cyan-400 rounded-full mt-2"></div>
                <p className="text-slate-200">{objetivo}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tecnologías */}
      <section className="bg-slate-900 border-y border-slate-800">
        <div className="max-w-7xl mx-auto px-6 py-20">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">
              Tecnologías Integradas
            </h2>

            <p className="text-slate-400 max-w-3xl mx-auto">
              El laboratorio utiliza plataformas modernas para desarrollar
              proyectos de automatización, monitoreo, análisis de datos y
              aprendizaje tecnológico.
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-4">
            {tecnologias.map((tech, index) => (
              <div
                key={index}
                className="px-5 py-3 bg-slate-800 border border-slate-700 rounded-2xl text-cyan-300 font-medium"
              >
                {tech}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Resultados */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-14">
          <h2 className="text-4xl font-bold mb-4">
            Resultados del Proyecto
          </h2>

          <p className="text-slate-400 max-w-3xl mx-auto">
            Los estudiantes que utilizaron el laboratorio mostraron una mejora
            significativa en comprensión tecnológica, resolución de problemas y
            participación activa.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8">
            <h3 className="text-5xl font-black text-cyan-400 mb-3">90%</h3>
            <p className="text-slate-300">Nivel de aprobación alcanzado</p>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8">
            <h3 className="text-5xl font-black text-cyan-400 mb-3">92%</h3>
            <p className="text-slate-300">Resolución correcta de problemas</p>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8">
            <h3 className="text-5xl font-black text-cyan-400 mb-3">97%</h3>
            <p className="text-slate-300">Interés por tecnologías emergentes</p>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8">
            <h3 className="text-5xl font-black text-cyan-400 mb-3">95%</h3>
            <p className="text-slate-300">Facilidad de uso del laboratorio</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950">
        <div className="max-w-7xl mx-auto px-6 py-10 flex flex-col md:flex-row justify-between items-center gap-4">
          <div>
            <h3 className="font-bold text-xl text-cyan-400">
              Laboratorio IoT
            </h3>
            <p className="text-slate-400 text-sm mt-1">
              Proyecto de divulgación científica y tecnológica.
            </p>
          </div>

          <div className="text-slate-500 text-sm text-center md:text-right">
            René Gil Alvarado y Martín Alejandro González Ramos
            <br />
            Coahuila, México · 2025
          </div>
        </div>
      </footer>
    </div>
  );
}
