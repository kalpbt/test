from db import init_db, SessionLocal
from models import Project, BOQItem


def main():
    # Initialize DB (create tables)
    # import Base from models and pass to init_db
    from models import Base as ModelsBase

    init_db(ModelsBase)
    print("Database tables created (or already exist).")

    # Demo: create a project + BOQ item using the SQLite fallback if no DATABASE_URL is set
    with SessionLocal() as session:
        proj = Project(name="Demo Project", brief="One-line brief for demo")
        session.add(proj)
        session.commit()
        session.refresh(proj)

        item = BOQItem(
            project_id=proj.id,
            item_name="Cement OPC 43",
            unit="bag",
            quantity=100,
            unit_rate=430.0,
            confidence=0.93,
        )
        session.add(item)
        session.commit()

    print("Demo project and BOQ item added.")


if __name__ == "__main__":
    main()
