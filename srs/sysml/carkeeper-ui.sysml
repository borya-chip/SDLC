package CarKeeperUI {
    doc /* Прототип пользовательского интерфейса CarKeeper в нотации SysML v2.
        Каждый экран — part def, наследующий Screen; его части — элементы
        интерфейса (поля, таблицы, кнопки), порядок частей задаёт компоновку.
        Мокапы srs/img/mock-*.png генерируются из этого файла скриптом
        srs/sysml/ui-render/render_ui.py. Версия 0.2. */

    private import ScalarValues::*;
    private import CarKeeperRequirements::*;

    // ---------- Библиотека элементов интерфейса ----------
    part def Widget {
        attribute label : String;
        attribute width : Integer;      // относительная ширина в строке
    }
    part def Screen :> Widget {
        attribute title : String;
        attribute subtitle : String;
        attribute activeMenu : String;  // выделенный пункт бокового меню
        attribute userInfo : String;
    }
    part def SideMenu :> Widget { attribute items : String; }
    part def Row :> Widget;             // дочерние элементы располагаются по горизонтали
    part def Card :> Widget;            // группа элементов с заголовком label
    part def Field :> Widget { attribute value : String; attribute required : Boolean; }
    part def Button :> Widget { attribute primary : Boolean; }
    part def Table :> Widget {
        attribute columns : String;     // через «|»
        attribute rows : String;        // строки через «;», ячейки через «|», [статус] — значок
    }
    part def CheckList :> Widget { attribute items : String; attribute checked : String; }
    part def Kpi :> Widget { attribute value : String; }
    part def BarChart :> Widget { attribute values : String; attribute captions : String; }
    part def Tabs :> Widget { attribute items : String; attribute active : String; }
    part def Note :> Widget;

    part mainMenu : SideMenu {
        attribute :>> items = "Панель|Мои автомобили|План ТО|Журнал|Расходы|Календарь|Администрирование";
    }

    // ---------- Экран «Панель» (REQ-FUNC-004, 008, 012) ----------
    part def DashboardScreen :> Screen {
        attribute :>> title = "Панель";
        attribute :>> subtitle = "Сегодня 01.11.2026 · 2 автомобиля";
        attribute :>> activeMenu = "Панель";
        attribute :>> userInfo = "owner@example.com · Пользователь";
        part addRecord : Button { attribute :>> label = "+ Запись в журнал"; attribute :>> primary = true; }
        part top : Row {
            part mileageCard : Card {
                attribute :>> label = "Ввод пробега"; attribute :>> width = 5;
                part car : Field { attribute :>> label = "Автомобиль"; attribute :>> value = "Skoda Octavia 1.6 MPI · 7777 AB-7"; }
                part line : Row {
                    part mileage : Field { attribute :>> label = "Текущий пробег, км *"; attribute :>> value = "56 000"; attribute :>> width = 3; }
                    part save : Button { attribute :>> label = "Сохранить пробег"; attribute :>> primary = true; attribute :>> width = 2; }
                }
                part hint : Note { attribute :>> label = "Предыдущее показание: 55 120 км (18.10.2026) · средний пробег 39 км/сут"; }
            }
            part counters : Card {
                attribute :>> label = "Статусы"; attribute :>> width = 2;
                part overdue : Kpi { attribute :>> label = "просрочено"; attribute :>> value = "2"; }
                part soon : Kpi { attribute :>> label = "скоро"; attribute :>> value = "3"; }
            }
            part notifications : Card {
                attribute :>> label = "Уведомления (3)"; attribute :>> width = 4;
                part list : CheckList {
                    attribute :>> items = "Салонный фильтр просрочен (Octavia)|Тормозная жидкость — до 15.11.2026|Страховка Polo истекает 30.11.2026|Пора менять шины на зимние";
                    attribute :>> checked = "4";
                }
            }
        }
        part upcoming : Card {
            attribute :>> label = "Предстоящие работы";
            part works : Table {
                attribute :>> columns = "Автомобиль|Работа|Срок|Осталось|Статус";
                attribute :>> rows = "Octavia|Замена салонного фильтра|20.10.2026|−12 дн.|[Просрочено];Polo|Замена ремня ГРМ|07.10.2026|−1 000 км|[Просрочено];Octavia|Замена тормозной жидкости|15.11.2026|14 дн.|[Скоро];Polo|Замена моторного масла|21.11.2026|800 км|[Скоро];Polo|Страховка (документ)|30.11.2026|29 дн.|[Скоро];Octavia|Замена моторного масла|09.02.2027|4 000 км|[В норме]";
            }
        }
    }

    // ---------- Экран «План ТО» (REQ-FUNC-006, 007, 008, 019) ----------
    part def PlanScreen :> Screen {
        attribute :>> title = "План ТО — Skoda Octavia 1.6 MPI";
        attribute :>> subtitle = "Регламент: бензин · пробег 56 000 км на 01.11.2026 · пороги 1000 км / 30 дней";
        attribute :>> activeMenu = "План ТО";
        attribute :>> userInfo = "owner@example.com · Пользователь";
        part thresholds : Button { attribute :>> label = "Пороги"; }
        part addItem : Button { attribute :>> label = "+ Добавить работу"; attribute :>> primary = true; }
        part items : Card {
            attribute :>> label = "Позиции плана";
            part plan : Table {
                attribute :>> columns = "Работа|Интервал|Последнее выполнение|Следующий срок|Статус";
                attribute :>> rows = "Замена салонного фильтра|15 000 км / 12 мес|20.10.2025 · 45 000 км|20.10.2026 (по времени)|[Просрочено];Замена тормозной жидкости|40 000 км / 24 мес|15.11.2024 · 30 000 км|15.11.2026 (по времени)|[Скоро];Замена моторного масла|10 000 км / 12 мес|10.03.2026 · 50 000 км|09.02.2027 (≈ 60 000 км)|[В норме];Замена масляного фильтра|10 000 км / 12 мес|10.03.2026 · 50 000 км|09.02.2027 (≈ 60 000 км)|[В норме];Проверка тормозных колодок|30 000 км / —|01.05.2026 · 50 000 км|23.06.2028 (≈ 80 000 км)|[В норме];Замена воздушного фильтра|30 000 км / 24 мес|10.03.2026 · 50 000 км|10.03.2028|[В норме];Замена ремня ГРМ|90 000 км / 60 мес|01.06.2023 · 20 000 км|01.06.2028|[В норме];Шины: зимние (Nokian, 12 400 км)|с 15.10 / с 01.04|18.10.2026 · 55 120 км|01.04.2027 — на летние|[В норме]";
            }
        }
        part disclaimer : Note { attribute :>> label = "Интервалы носят рекомендательный характер. Сверяйтесь с руководством по эксплуатации."; }
    }

    // ---------- Экран «Новая запись журнала» (REQ-FUNC-009, 010, 013) ----------
    part def RecordScreen :> Screen {
        attribute :>> title = "Новая запись журнала";
        attribute :>> subtitle = "Skoda Octavia 1.6 MPI";
        attribute :>> activeMenu = "Журнал";
        attribute :>> userInfo = "owner@example.com · Пользователь";
        part cancel : Button { attribute :>> label = "Отмена"; }
        part save : Button { attribute :>> label = "Сохранить"; attribute :>> primary = true; }
        part main : Card {
            attribute :>> label = "Основные данные";
            part line : Row {
                part date : Field { attribute :>> label = "Дата *"; attribute :>> value = "01.11.2026"; }
                part mileage : Field { attribute :>> label = "Пробег, км *"; attribute :>> value = "56 000"; }
                part place : Field { attribute :>> label = "Где выполнено"; attribute :>> value = "СТО «АвтоМастер»"; attribute :>> width = 2; }
            }
        }
        part middle : Row {
            part closes : Card {
                attribute :>> label = "Выполненные позиции плана"; attribute :>> width = 2;
                part items : CheckList {
                    attribute :>> items = "Замена салонного фильтра|Замена тормозной жидкости|Замена моторного масла|Замена масляного фильтра";
                    attribute :>> checked = "1|2";
                }
            }
            part partsCard : Card {
                attribute :>> label = "Расходники"; attribute :>> width = 5;
                part parts : Table {
                    attribute :>> columns = "Наименование|Производитель|Артикул|Кол-во|Цена, BYN";
                    attribute :>> rows = "Фильтр салонный угольный|Mann-Filter|CUK 2939|1|38,00;Тормозная жидкость DOT 4, 1 л|ATE|03.9901-6402.2|1|32,50;+ добавить расходник||||";
                }
                part totals : Row {
                    part labour : Field { attribute :>> label = "Стоимость работ, BYN"; attribute :>> value = "60,00"; }
                    part total : Field { attribute :>> label = "Итого, BYN"; attribute :>> value = "130,50"; }
                }
            }
        }
        part extra : Row {
            part commentField : Field { attribute :>> label = "Комментарий"; attribute :>> value = "Проверить передние колодки при следующем ТО"; attribute :>> width = 3; }
            part attach : Field { attribute :>> label = "Вложения (JPEG, PNG, PDF ≤ 10 МБ)"; attribute :>> value = "chek_011126.jpg  + прикрепить"; attribute :>> width = 2; }
        }
    }

    // ---------- Экран «Расходы» (REQ-FUNC-014, 015, 018) ----------
    part def ExpensesScreen :> Screen {
        attribute :>> title = "Расходы";
        attribute :>> subtitle = "Skoda Octavia 1.6 MPI · 01.11.2025 – 31.10.2026";
        attribute :>> activeMenu = "Расходы";
        attribute :>> userInfo = "owner@example.com · Пользователь";
        part csv : Button { attribute :>> label = "Экспорт CSV"; }
        part pdf : Button { attribute :>> label = "Экспорт истории в PDF"; attribute :>> primary = true; }
        part kpis : Row {
            part total : Kpi { attribute :>> label = "Всего за период"; attribute :>> value = "1 284,50 BYN"; }
            part distance : Kpi { attribute :>> label = "Пробег за период"; attribute :>> value = "14 200 км"; }
            part perKm : Kpi { attribute :>> label = "Стоимость 1 км"; attribute :>> value = "0,09 BYN"; }
            part forecast : Kpi { attribute :>> label = "Прогноз на 12 мес."; attribute :>> value = "≈ 740 BYN"; }
        }
        part charts : Row {
            part byMonth : Card {
                attribute :>> label = "По месяцам, BYN"; attribute :>> width = 3;
                part chart : BarChart {
                    attribute :>> values = "64|21|0|32|412|86|11|107|0|21|171|54";
                    attribute :>> captions = "11|12|01|02|03|04|05|06|07|08|09|10";
                }
            }
            part byCategory : Card {
                attribute :>> label = "По категориям"; attribute :>> width = 2;
                part categories : Table {
                    attribute :>> columns = "Категория|Сумма, BYN|Доля";
                    attribute :>> rows = "Жидкости|395,00|31 %;Тормоза|248,00|19 %;Двигатель|215,00|17 %;Фильтры|186,50|15 %;Шины|120,00|9 %;Прочее|120,00|9 %;Итого|1 284,50|100 %";
                }
            }
        }
    }

    // ---------- Экран «Регламенты ТО» (REQ-FUNC-005) ----------
    part def AdminRegulationsScreen :> Screen {
        attribute :>> title = "Регламенты ТО";
        attribute :>> subtitle = "Изменения не затрагивают уже созданные планы автомобилей";
        attribute :>> activeMenu = "Администрирование";
        attribute :>> userInfo = "admin@example.com · Администратор";
        part add : Button { attribute :>> label = "+ Добавить работу"; attribute :>> primary = true; }
        part engine : Tabs { attribute :>> items = "Бензин|Дизель|Гибрид|Электро"; attribute :>> active = "Бензин"; }
        part list : Card {
            attribute :>> label = "Работы регламента";
            part items : Table {
                attribute :>> columns = "Работа|Категория|Интервал, км|Интервал, мес.|В планах";
                attribute :>> rows = "Замена моторного масла|Жидкости|10 000|12|1 284;Замена масляного фильтра|Фильтры|10 000|12|1 284;Замена воздушного фильтра|Фильтры|30 000|24|1 280;Замена салонного фильтра|Фильтры|15 000|12|1 271;Замена свечей зажигания|Двигатель|30 000|36|1 262;Замена тормозной жидкости|Тормоза|40 000|24|1 284;Проверка/замена колодок|Тормоза|30 000|—|1 284;Замена охлаждающей жидкости|Жидкости|60 000|48|1 250;Замена масла в КПП|Жидкости|60 000|48|977;Замена ремня ГРМ|Двигатель|90 000|60|812";
            }
        }
        part rule : Note { attribute :>> label = "Должен быть задан хотя бы один интервал (REQ-FUNC-005)."; }
    }

    // ---------- Навигация между экранами ----------
    part def CarKeeperWebUI {
        part dashboard : DashboardScreen;
        part plan : PlanScreen;
        part record : RecordScreen;
        part expenses : ExpensesScreen;
        part admin : AdminRegulationsScreen;

        first dashboard then plan;      // клик по работе на панели
        first plan then record;         // кнопка «Выполнено»
        first record then plan;         // после сохранения записи
        first dashboard then expenses;
        first dashboard then admin;     // только для администратора
    }

    // ---------- Связь экранов с требованиями ----------
    part ui : CarKeeperWebUI;
    satisfy carKeeperSpec.garageGroup.func004 by ui.dashboard;
    satisfy carKeeperSpec.planGroup.func008 by ui.dashboard;
    satisfy carKeeperSpec.reminderGroup.func012 by ui.dashboard;
    satisfy carKeeperSpec.planGroup.func006 by ui.plan;
    satisfy carKeeperSpec.planGroup.func007 by ui.plan;
    satisfy carKeeperSpec.garageGroup.func019 by ui.plan;
    satisfy carKeeperSpec.journalGroup.func009 by ui.record;
    satisfy carKeeperSpec.journalGroup.func010 by ui.record;
    satisfy carKeeperSpec.journalGroup.func013 by ui.record;
    satisfy carKeeperSpec.reportGroup.func014 by ui.expenses;
    satisfy carKeeperSpec.reportGroup.func015 by ui.expenses;
    satisfy carKeeperSpec.reportGroup.func018 by ui.expenses;
    satisfy carKeeperSpec.planGroup.func005 by ui.admin;
}
