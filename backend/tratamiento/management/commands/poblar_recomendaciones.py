# tratamiento/management/commands/poblar_recomendaciones.py
from django.core.management.base import BaseCommand
from tratamiento.models import Recomendacion


class Command(BaseCommand):
    help = 'Pobla la base de datos con recomendaciones predefinidas para migraña'

    def handle(self, *args, **options):
        # Recomendaciones generales (para ambos géneros)
        recomendaciones_generales = [
            {
                'clave': 'rutina_sueno',
                'descripcion': 'Mantener una rutina regular de sueño: Dormir entre 7-9 horas por noche ayuda a prevenir los episodios de migraña.',
                'aplicable_a': 'both'
            },
            {
                'clave': 'ejercicio_moderado',
                'descripcion': 'Realizar ejercicio de forma moderada: La actividad física regular puede reducir la frecuencia de los episodios, pero evitar el ejercicio excesivo.',
                'aplicable_a': 'both'
            },
            {
                'clave': 'control_estres',
                'descripcion': 'Controlar los niveles de estrés: Técnicas de relajación como la meditación, respiración profunda o yoga son útiles para reducir el estrés y, por ende, disminuir la frecuencia de las migrañas.',
                'aplicable_a': 'both'
            },
            {
                'clave': 'hidratacion_adecuada',
                'descripcion': 'Mantener una hidratación adecuada: Beber suficiente agua a lo largo del día es esencial para prevenir la deshidratación, que puede ser un factor desencadenante de las migrañas.',
                'aplicable_a': 'both'
            },
            {
                'clave': 'ambiente_oscuro_silencioso',
                'descripcion': 'Buscar un ambiente oscuro y silencioso para descansar durante el episodio. Usar gafas de sol o viseras oscuras si es necesario.',
                'aplicable_a': 'both'
            },
            {
                'clave': 'compresion_fria_tibia',
                'descripcion': 'Realizar una compresión fría o tibia sobre la zona afectada puede aliviar el dolor pulsátil.',
                'aplicable_a': 'both'
            },
            {
                'clave': 'evitar_esfuerzo_fisico',
                'descripcion': 'Si la migraña empeora con la actividad: Evitar cualquier tipo de esfuerzo físico mientras dure el episodio, ya que el ejercicio excesivo puede intensificar el dolor.',
                'aplicable_a': 'both'
            },
            {
                'clave': 'manejo_nauseas_vomitos',
                'descripcion': 'Si el paciente tiene náuseas o vómitos: Ingerir líquidos en pequeñas cantidades y evitar alimentos pesados. Los medicamentos antieméticos pueden ser indicados bajo supervisión médica.',
                'aplicable_a': 'both'
            }
        ]

        # Recomendaciones específicas para mujeres
        recomendaciones_mujeres = [
            {
                'clave': 'migraña_menstrual',
                'descripcion': 'Si está menstruando o en fase premenstrual: Utilizar analgésicos adecuados (como el ibuprofeno) y practicar técnicas de relajación pueden ayudar a aliviar los episodios menstruales.',
                'aplicable_a': 'female'
            },
            {
                'clave': 'anticonceptivos_hormonales',
                'descripcion': 'Consultar con un ginecólogo sobre anticonceptivos hormonales: Algunos anticonceptivos hormonales pueden influir en la frecuencia de las migrañas. Es recomendable discutir alternativas o ajustes con un especialista si se observa esta relación.',
                'aplicable_a': 'female'
            }
        ]

        todas_recomendaciones = recomendaciones_generales + recomendaciones_mujeres

        creadas = 0
        actualizadas = 0

        for rec_data in todas_recomendaciones:
            recomendacion, created = Recomendacion.objects.get_or_create(
                clave=rec_data['clave'],
                defaults={
                    'descripcion': rec_data['descripcion'],
                    'aplicable_a': rec_data['aplicable_a']
                }
            )

            if created:
                creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creada: {rec_data["clave"]}')
                )
            else:
                # Actualizar si ya existe pero con datos diferentes
                if (recomendacion.descripcion != rec_data['descripcion'] or
                        recomendacion.aplicable_a != rec_data['aplicable_a']):
                    recomendacion.descripcion = rec_data['descripcion']
                    recomendacion.aplicable_a = rec_data['aplicable_a']
                    recomendacion.save()
                    actualizadas += 1
                    self.stdout.write(
                        self.style.WARNING(f'↻ Actualizada: {rec_data["clave"]}')
                    )
                else:
                    self.stdout.write(
                        self.style.HTTP_INFO(f'- Ya existe: {rec_data["clave"]}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n Proceso completado:\n'
                f'   • {creadas} recomendaciones creadas\n'
                f'   • {actualizadas} recomendaciones actualizadas\n'
                f'   • {len(todas_recomendaciones)} recomendaciones en total'
            )
        )