package CarKeeperRequirements {
    doc /* Требования к веб-приложению CarKeeper (планировщик ТО автомобиля).
        Версия 0.2 (после рецензирования). */

    private import ScalarValues::*;

    // ---------- Участники и система ----------
    part def Owner;          // пользователь — владелец автомобиля
    part def Administrator;
    part def MailServer;     // внешний SMTP-сервер

    part def CarKeeper {
        part accountModule;
        part garageModule;
        part planModule;
        part dueDateCalculator;   // ядро: расчёт сроков и статусов
        part journalModule;
        part notificationModule;
        part reportModule;
    }

    // ---------- Базовые определения требований ----------
    requirement def FunctionalRequirement {
        attribute priority : String;   // MoSCoW: Must | Should | Could
        attribute iteration : Integer;
        subject system : CarKeeper;
    }
    requirement def QualityRequirement {
        attribute metric : String;
        subject system : CarKeeper;
    }

    // ---------- Функциональные требования ----------
    requirement carKeeperSpec {
        doc /* Корневое требование: вести историю обслуживания автомобиля,
            планировать замену расходников и напоминать о предстоящем ТО. */

        requirement accessAndRoles {
            requirement <'REQ-FUNC-001'> func001 : FunctionalRequirement {
                doc /* Регистрация и вход. */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-002'> func002 : FunctionalRequirement {
                doc /* Роли и права доступа. */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
        }

        requirement garageGroup {
            requirement <'REQ-FUNC-003'> func003 : FunctionalRequirement {
                doc /* Управление автомобилями. */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-004'> func004 : FunctionalRequirement {
                doc /* Ввод показаний пробега; v = (M2 - M1) / (D2 - D1). */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-019'> func019 : FunctionalRequirement {
                doc /* Сезонная смена шин (добавлено в v0.2). */
                attribute :>> priority = "Should"; attribute :>> iteration = 2;
            }
            requirement <'REQ-FUNC-020'> func020 : FunctionalRequirement {
                doc /* Сроки документов: страховка, техосмотр (добавлено в v0.2). */
                attribute :>> priority = "Should"; attribute :>> iteration = 2;
            }
        }

        requirement planGroup {
            requirement <'REQ-FUNC-005'> func005 : FunctionalRequirement {
                doc /* Справочник регламентов ТО. */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-006'> func006 : FunctionalRequirement {
                doc /* План ТО автомобиля. */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-007'> func007 : FunctionalRequirement {
                doc /* Срок = min(D_last + T, D_cur + (M_last + L - M_cur) / v). */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-008'> func008 : FunctionalRequirement {
                doc /* Статусы: В норме / Скоро (1000 км или 30 дней) / Просрочено. */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
        }

        requirement journalGroup {
            requirement <'REQ-FUNC-009'> func009 : FunctionalRequirement {
                doc /* Запись в журнал (v0.2: производитель и артикул расходника). */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-010'> func010 : FunctionalRequirement {
                doc /* Закрытие позиций плана записью журнала. */
                attribute :>> priority = "Must"; attribute :>> iteration = 1;
            }
            requirement <'REQ-FUNC-013'> func013 : FunctionalRequirement {
                doc /* Вложения к записи: JPEG, PNG, PDF до 10 МБ. */
                attribute :>> priority = "Could"; attribute :>> iteration = 3;
            }
        }

        requirement reminderGroup {
            requirement <'REQ-FUNC-011'> func011 : FunctionalRequirement {
                doc /* Напоминания по e-mail. */
                attribute :>> priority = "Should"; attribute :>> iteration = 2;
            }
            requirement <'REQ-FUNC-012'> func012 : FunctionalRequirement {
                doc /* Уведомления в приложении. */
                attribute :>> priority = "Should"; attribute :>> iteration = 2;
            }
            requirement <'REQ-FUNC-016'> func016 : FunctionalRequirement {
                doc /* Календарь предстоящих работ на 12 месяцев. */
                attribute :>> priority = "Should"; attribute :>> iteration = 2;
            }
        }

        requirement reportGroup {
            requirement <'REQ-FUNC-014'> func014 : FunctionalRequirement {
                doc /* Отчёт о расходах за период. */
                attribute :>> priority = "Should"; attribute :>> iteration = 2;
            }
            requirement <'REQ-FUNC-015'> func015 : FunctionalRequirement {
                doc /* Экспорт истории в PDF. */
                attribute :>> priority = "Could"; attribute :>> iteration = 3;
            }
            requirement <'REQ-FUNC-017'> func017 : FunctionalRequirement {
                doc /* Импорт и экспорт журнала в CSV. */
                attribute :>> priority = "Could"; attribute :>> iteration = 3;
            }
            requirement <'REQ-FUNC-018'> func018 : FunctionalRequirement {
                doc /* Прогноз расходов на 12 месяцев. */
                attribute :>> priority = "Could"; attribute :>> iteration = 3;
            }
        }
    }

    // ---------- Нефункциональные требования ----------
    requirement qualitySpec {
        requirement <'REQ-PERF-001'> perf001 : QualityRequirement {
            attribute :>> metric = "Ответ страницы <= 1,5 с для 95 % запросов";
        }
        requirement <'REQ-PERF-002'> perf002 : QualityRequirement {
            attribute :>> metric = "Пересчёт плана <= 1 с";
        }
        requirement <'REQ-PERF-003'> perf003 : QualityRequirement {
            attribute :>> metric = "PDF на 200 записей <= 5 с";
        }
        requirement <'REQ-PERF-004'> perf004 : QualityRequirement {
            attribute :>> metric = "Проверка 10 000 автомобилей <= 10 мин";
        }
        requirement <'REQ-SEC-001'> sec001 : QualityRequirement {
            attribute :>> metric = "bcrypt, стоимость >= 10";
        }
        requirement <'REQ-SEC-003'> sec003 : QualityRequirement {
            attribute :>> metric = "Чужие объекты -> 404";
        }
        requirement <'REQ-SEC-004'> sec004 : QualityRequirement {
            attribute :>> metric = "Сеанс 30 мин; 5 попыток -> блокировка 15 мин";
        }
        requirement <'REQ-REL-001'> rel001 : QualityRequirement {
            attribute :>> metric = "Напоминание не дублируется";
        }
        requirement <'REQ-REL-002'> rel002 : QualityRequirement {
            attribute :>> metric = "3 повтора SMTP: 1, 5, 25 мин";
        }
        requirement <'REQ-AVAIL-001'> avail001 : QualityRequirement {
            attribute :>> metric = "Доступность >= 99 % в месяц";
        }
        requirement <'REQ-MAINT-001'> maint001 : QualityRequirement {
            attribute :>> metric = "Покрытие модуля расчёта >= 90 %";
        }
        requirement <'REQ-COST-001'> cost001 : QualityRequirement {
            attribute :>> metric = "Хостинг <= 10 USD/мес";
        }
        // полный перечень — раздел 3.3–3.5 файла srs.md
    }

    // ---------- Варианты использования ----------
    use case def AddCar        { subject system : CarKeeper; actor owner : Owner; }
    use case def EnterMileage  { subject system : CarKeeper; actor owner : Owner; }
    use case def ViewPlan      { subject system : CarKeeper; actor owner : Owner; }
    use case def AddRecord     { subject system : CarKeeper; actor owner : Owner; }
    use case def CloseItems    { subject system : CarKeeper; actor owner : Owner; }
    use case def ViewExpenses  { subject system : CarKeeper; actor owner : Owner; }
    use case def ExportPdf     { subject system : CarKeeper; actor owner : Owner; }
    use case def ManageTyres   { subject system : CarKeeper; actor owner : Owner; }
    use case def TrackDocuments{ subject system : CarKeeper; actor owner : Owner; }
    use case def ManageRegulations { subject system : CarKeeper; actor admin : Administrator; }
    use case def SendReminders {
        subject system : CarKeeper;
        actor owner : Owner;
        actor mail : MailServer;
    }

    // Сводный вариант использования для диаграммы (рисунок 3.1)
    use case carKeeperUseCases {
        subject system : CarKeeper;
        actor owner : Owner;
        actor admin : Administrator;
        actor mail : MailServer;
        include use case addCar : AddCar;
        include use case viewPlan : ViewPlan {
            include use case enterMileage : EnterMileage;
        }
        include use case addRecord : AddRecord {
            include use case closeItems : CloseItems;
        }
        include use case viewExpenses : ViewExpenses {
            include use case exportPdf : ExportPdf;
        }
        include use case manageTyres : ManageTyres;
        include use case trackDocuments : TrackDocuments;
        include use case sendReminders : SendReminders;
        include use case manageRegulations : ManageRegulations;
    }

    use case addRecord : AddRecord {
        include use case closeItems : CloseItems;
    }
    use case viewPlan : ViewPlan {
        include use case enterMileage : EnterMileage;
    }

    // ---------- Удовлетворение требований ----------
    part carKeeper : CarKeeper;
    satisfy carKeeperSpec.planGroup.func007 by carKeeper.dueDateCalculator;
    satisfy carKeeperSpec.planGroup.func008 by carKeeper.dueDateCalculator;
    satisfy carKeeperSpec.reminderGroup.func011 by carKeeper.notificationModule;
    satisfy carKeeperSpec.reportGroup.func014 by carKeeper.reportModule;
    satisfy carKeeperSpec.journalGroup.func009 by carKeeper.journalModule;
}
