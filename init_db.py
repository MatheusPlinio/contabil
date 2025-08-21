from database.config import Base, engine
from models import upload


def init_db():
    print("🔧 Criando tabelas no banco...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")


if __name__ == "__main__":
    init_db()
