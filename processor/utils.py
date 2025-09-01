
import re
from collections import Counter
from typing import List, Set
STOPWORDS = set('''и в во не что он на я с со как а то все она так его но да ты к у же вы за бы по ее мне было вот от меня еще нет о из ему теперь когда даже ну вдруг ли если уже или ни быть был него до вас нибудь опять уж вам сказал ведь там потом себя ничего ей может они тут где есть надо ней для мы тебя их чем была сам чтоб без будто чего раз тоже себе под будет ж тогда кто этот того потому этого какой совсем ним здесь этом один почти мой тем чтобы нее сейчас были куда зачем всех никогда можно при наконец два об другой хоть после над больше тот через эти нас про всего них какая много разве три эту моя впрочем хорошо свою этой перед иногда лучше чуть том нельзя такой им более всегда конечно всю между de la que el en y a los del se las por un para con no una su al lo como más pero sus le ya o este sí porque esta entre cuando muy sin sobre también me hasta hay donde quien desde todo nos durante todos uno les ni contra otros ese eso ante ellos e esto mí antes algunos qué unos yo otro otras otra él tanto esa estos mucho quienes nada muchos cual poco ella estar estas algunas algo está mi mis tú te ti tu tus ellas nosotros nosotras vosotros vosotras si mío mия míos mías tuyo tuya tuyos tuyas suyo suya suyos suyas nuestro nuestra nuestros nuestras vuestro vuestros estoy estás está estamos estáis están the be to of and a in that have i it for not on with he as you do at this but his by from they we say her she or an will my one all would there their'''.split())
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁёÁÉÍÓÚÑáéíóúñÜü0-9']+")
def tokenize(text: str):
    text = text.lower()
    words = WORD_RE.findall(text)
    return [w for w in words if w not in STOPWORDS and not w.isdigit()]
