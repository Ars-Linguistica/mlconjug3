import mlconjug3

default_conjugator = mlconjug3.Conjugator("es")
conjug_info = default_conjugator.conjugate("correr").conjug_info
gerund = conjug_info["Gerundio"]
print(gerund)
