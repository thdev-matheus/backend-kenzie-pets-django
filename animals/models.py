from math import log  # método que calcula os logarítmos da biblioteca math do python

from django.db import models


# Model de escolhas que herda de textChoices. São como as options de um select no HTML
class AnimalSex(models.TextChoices):
    MACHO = "Macho"
    FEMEA = "Fêmea"
    NAO_INFORMADO = "Não Informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    # definindo que a coluna "sex" será uma das escolhas da classe acima e tbm definindo um default garantindo assim que sempre será um campo preenchido
    sex = models.CharField(
        max_length=15, choices=AnimalSex.choices, default=AnimalSex.NAO_INFORMADO
    )

    # relação N:1 a chave fica sempre do lado N da relação, o seja um animal pode pertencer a apenas 1 grupo mas o mesmo grupo pode representar vários animais.
    # Deve ser passada a model da outra parte da relação e podemos iportar e passar direto ou passar o "caminho" onde essa model está dizendo o app a qual pertence e o nome da model, a regra de deleção e como parâmetro opcional o nome que estará do outro lado da relação e caso não seja passado será criado com o nome "<nome_da_model>_set", ou seja, um conjunto de models. Neste caso seria "animal_set".
    # É extremamente importante que não se modifique o nome do módulo "models.py" nos apps criados. Inclusive, pelo menos até agora não há a necessidade de renomear ou mudar de lugar(tirando os testes) os módulos criados.
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="animals"
    )

    # Relação muitos pra muitos. Pode ser colocada em qualquer uma das partes do relacionamento. deverá ser passado a model ou o "caminho" e não precisa da regra de deleção porque fica implícito que numa relação N:N quando se deleta a outra parte deve-se excluir apenas a relação e não destruir o objeto na tabela.
    traits = models.ManyToManyField("traits.Trait", related_name="animals")

    # método de instância que não armazena no banco a informação mas que pode ser usado para calcular ou criar uma informação a partir do que é pego no banco. pode ser usado por exemplo para calcular a idade de uma pessoa a partir da sua data de nascimento.
    def convert_dog_age_to_human_years(self) -> float:
        HUMAN_AGE = 16 * log(self.age) + 31

        return round(HUMAN_AGE, 1)
