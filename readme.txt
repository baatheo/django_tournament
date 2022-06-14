Django turniej Bartosz Porębski  127314 Readme :)

ogólne założenia:
- w przypadku liczby drużyn nie odpowiadającej potęgi 2, losujemy tak zwanych szczęsciarzy.
Nie są oni widoczni w konkretnym etapie, dopiero przy następnym etapie są dopasowywani do meczów.
- Wyniki meczów nie mogą być remisowe ( zablokowane na bazie, niestety na frontendzie nie), więc
prosiłbym o nie wpisywanie wyników remisowych.
- W widoku meczu na górze są pokazane aktualne etapy gry.
- Mecze trzeba zatwierdzać pojedyńczo, a następnie zatwierdzić cały etap by wygenerować kolejny.
- Kolejne etapy są zawsze losowe.

accountmanagent - sekcja do zarządzania uzytkownikami (logowanie, rejestracja)
frontend - wiadomo :)
tournament - głowna paczka projektu
tournamentbe - paczka do zarządzania turniejem
