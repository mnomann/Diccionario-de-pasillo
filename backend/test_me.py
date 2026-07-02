import asyncio, traceback
from sqlalchemy import func, select
from app.database import async_session_maker
from app.models.sugerencia import Sugerencia
from app.models.usuario import Usuario

async def test():
    async with async_session_maker() as db:
        # Simulate get_current_user
        result = await db.execute(select(Usuario).where(Usuario.id == 1))
        usuario = result.scalar_one_or_none()
        print(f'Usuario: {usuario.nombre}, es_admin: {usuario.es_admin}')
        
        try:
            # Count
            count_result = await db.execute(
                select(func.count()).select_from(
                    select(Sugerencia).where(Sugerencia.usuario_id == usuario.id).subquery()
                )
            )
            total_sugerencias = count_result.scalar_one()
            print(f'Total: {total_sugerencias}')
            
            # Group by
            estado_result = await db.execute(
                select(Sugerencia.estado, func.count().label("cantidad"))
                .where(Sugerencia.usuario_id == usuario.id)
                .group_by(Sugerencia.estado)
            )
            sugerencias_por_estado = {
                row.estado: row.cantidad for row in estado_result.all()
            }
            print(f'Por estado: {sugerencias_por_estado}')
            
            # Build response
            from app.schemas.usuario import UsuarioMe
            estadisticas = {
                "total_sugerencias": total_sugerencias,
                "sugerencias_por_estado": sugerencias_por_estado,
            }
            
            me = UsuarioMe(
                id=usuario.id,
                nombre=usuario.nombre,
                email=usuario.email,
                fecha_registro=usuario.fecha_registro,
                es_admin=usuario.es_admin,
                preferencias=usuario.preferencias,
                ultima_conexion=usuario.ultima_conexion,
                estadisticas=estadisticas,
            )
            print(f'\nUsuarioMe response: {me.model_dump_json(indent=2)}')
        except Exception as e:
            traceback.print_exc()

asyncio.run(test())
