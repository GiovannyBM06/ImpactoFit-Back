# Estructura del backend (Claude)

impactofit_backend/
│
├── main.py                          # Punto de entrada, registro de routers  
├── requirements.txt  
├── .env  
├── alembic.ini                      # Configuración de migraciones  
│  
│  
├── core/                            # Configuración transversal  
│   ├── __init__.py  
│   ├── config.py                    # Variables de entorno (.env)  
│   ├── dependencies.py              # Registro global de Depends()  
│   └── security.py                  # JWT: generar y verificar tokens  
│  
│  
├── api/                             # ← CAPA PRESENTACIÓN  
│   ├── __init__.py  
│   │  
│   ├── controllers/                 # Routers FastAPI (un archivo por entidad)  
│   │   ├── __init__.py  
│   │   ├── auth_controller.py       # POST /login, POST /logout, POST /recuperar-password  
│   │   ├── usuario_controller.py    # CRUD usuarios (admin)  
│   │   ├── asistencia_controller.py # POST /asistencia (cliente)  
│   │   ├── rutina_controller.py     # GET /rutina, PUT /ejercicios (entrenador)  
│   │   ├── membresia_controller.py  # PUT /activar, POST /comprobante (admin)  
│   │   └── clase_controller.py      # POST /clase, POST /inscripcion (admin/cliente)  
│   │  
│   ├── schemas/                     # DTOs Pydantic — Request y Response  
│   │   ├── __init__.py
│   │   ├── auth_schema.py           # LoginRequest, TokenResponse  
│   │   ├── usuario_schema.py        # UsuarioRequest, UsuarioResponse  
│   │   ├── asistencia_schema.py
│   │   ├── rutina_schema.py         # RutinaResponse, EjercicioRequest  
│   │   ├── membresia_schema.py      # ActivarMembresiaRequest, ComprobanteResponse  
│   │   └── clase_schema.py          # ClaseRequest, InscripcionRequest  
│   │  
│   └── middlewares/  
│       ├── __init__.py  
│       ├── auth_middleware.py        # Verificación JWT en cada request  
│       └── error_handler.py         # Manejo global de excepciones  
│  
│  
├── domain/                          # ← CAPA DE NEGOCIO  
│   ├── __init__.py  
│   │  
│   ├── entities/                    # Modelos SQLAlchemy  
│   │   ├── __init__.py  
│   │   ├── audit_base.py            # AuditBase: id, created_at, updated_at  
│   │   ├── usuario.py               # Usuario: nombre, email, password, rol  
│   │   ├── membresia.py             # Membresia: tipo, fecha_inicio, fecha_fin, estado  
│   │   ├── asistencia.py            # Asistencia: usuario_id, fecha, formulario  
│   │   ├── rutina.py                # Rutina: usuario_id, entrenador_id  
│   │   ├── ejercicio.py             # Ejercicio: rutina_id, nombre, series, reps  
│   │   └── clase_grupal.py          # ClaseGrupal: nombre, cupo_max, cupo_actual  
│   │  
│   ├── enums/  
│   │   ├── __init__.py  
│   │   ├── rol_enum.py              # CLIENTE, ENTRENADOR, ADMINISTRADOR  
│   │   ├── membresia_tipo_enum.py   # MENSUAL, TRIMESTRAL, ANUAL  
│   │   └── membresia_estado_enum.py # PENDIENTE, ACTIVA, VENCIDA  
│   │
│   │
│   ├── interfaces/                  # Contratos (Principio de Inversión de Dependencias)  
│   │   ├── __init__.py  
│   │   │  
│   │   ├── repositories/            # Lo que el Domain le exige al DataAccess  
│   │   │   ├── __init__.py  
│   │   │   ├── i_repository.py      # IRepository genérico (base)  
│   │   │   ├── i_usuario_repository.py  
│   │   │   ├── i_membresia_repository.py  
│   │   │   ├── i_rutina_repository.py  
│   │   │   ├── i_asistencia_repository.py  
│   │   │   └── i_clase_repository.py  
│   │   │  
│   │   └── services/                # Lo que el API le exige al Domain  
│   │       ├── __init__.py  
│   │       ├── i_auth_service.py  
│   │       ├── i_usuario_service.py  
│   │       ├── i_membresia_service.py  
│   │       ├── i_rutina_service.py  
│   │       ├── i_asistencia_service.py  
│   │       └── i_clase_service.py  
│   │  
│   │  
│   ├── services/                    # Implementaciones de lógica de negocio  
│   │   ├── __init__.py  
│   │   ├── auth_service.py          # Login, JWT, recuperar contraseña  
│   │   ├── usuario_service.py       # Crear usuario usando UsuarioFactory  
│   │   ├── membresia_service.py     # Activar membresía usando Strategy + Observer  
│   │   ├── rutina_service.py        # Ver/modificar rutina usando Template Method  
│   │   ├── asistencia_service.py    # Registrar asistencia usando Template Method  
│   │   └── clase_service.py         # Crear clase, inscribir usando Observer  
│   │  
│   │  
│   ├── patterns/                    # ← PATRONES GoF EXPLÍCITOS  
│   │   ├── __init__.py  
│   │   │  
│   │   ├── factory/                 # PATRÓN: Factory Method  
│   │   │   ├── __init__.py  
│   │   │   ├── usuario_factory.py   # Clase abstracta UsuarioFactory  
│   │   │   ├── cliente_factory.py   # Crea Usuario con rol CLIENTE  
│   │   │   ├── entrenador_factory.py# Crea Usuario con rol ENTRENADOR  
│   │   │   └── admin_factory.py     # Crea Usuario con rol ADMINISTRADOR  
│   │   │  
│   │   ├── strategy/                # PATRÓN: Strategy  
│   │   │   ├── __init__.py  
│   │   │   ├── i_membresia_strategy.py  # Interfaz base  
│   │   │   ├── mensual_strategy.py      # Calcula vencimiento +30 días  
│   │   │   ├── trimestral_strategy.py   # Calcula vencimiento +90 días  
│   │   │   └── anual_strategy.py        # Calcula vencimiento +365 días  
│   │   │
│   │   ├── observer/                # PATRÓN: Observer  
│   │   │   ├── __init__.py  
│   │   │   ├── i_observer.py        # Interfaz Observer base  
│   │   │   ├── i_observable.py      # Interfaz Observable base  
│   │   │   ├── membresia_event.py   # Evento: MembresiaActivada  
│   │   │   ├── clase_event.py       # Evento: CupoAgotado  
│   │   │   ├── comprobante_observer.py  # Suscriptor: genera comprobante  
│   │   │   └── estado_usuario_observer.py # Suscriptor: activa usuario  
│   │   │  
│   │   └── template/                # PATRÓN: Template Method  
│   │       ├── __init__.py  
│   │       ├── registro_base.py     # Esqueleto: validar → verificar membresía → registrar  
│   │       ├── registro_asistencia.py   # Implementación concreta  
│   │       └── registro_inscripcion.py  # Implementación concreta  
│
│
├── data_access/                     # ← CAPA DE DATOS  
│   ├── __init__.py  
│   │  
│   ├── context/  
│   │   ├── __init__.py  
│   │   └── database.py              # DatabaseManager (Singleton implícito via SQLAlchemy)  
│   │  
│   ├── repositories/                # Implementaciones concretas de las interfaces  
│   │   ├── __init__.py  
│   │   ├── base_repository.py       # PATRÓN: Repository genérico  
│   │   ├── usuario_repository.py    # Extiende base, implementa IUsuarioRepository  
│   │   ├── membresia_repository.py  
│   │   ├── rutina_repository.py  
│   │   ├── asistencia_repository.py  
│   │   └── clase_repository.py  
│   │  
│   └── migrations/                  # Alembic (generado automáticamente)  
│       ├── env.py  
│       ├── script.py.mako  
│       └── versions/  
│           └── ...  
│  
│  
└── tests/                           # Pruebas (opcional para el MVP)  
    ├── __init__.py  
    ├── test_auth.py  
    ├── test_membresia.py  
    └── test_rutina.py  