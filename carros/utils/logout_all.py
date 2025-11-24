def logout_all_sessions():
    from django.contrib.sessions.models import Session

    print("\n[SIG-LOGOUT] Encerrando todas as sessões ativas...")
    try:
        deleted_count, _ = Session.objects.all().delete()
        print(f"[SIG-LOGOUT] Sucesso! {deleted_count} sessões foram encerradas.")
    except Exception as e:
        print(f"[SIG-LOGOUT] Erro ao limpar sessões: {e}. Verifique se as migrações foram aplicadas.")