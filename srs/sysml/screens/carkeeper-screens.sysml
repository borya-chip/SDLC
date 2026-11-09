package CarKeeper_Dashboard {
    part def DashboardPage {
        attribute title = "CarKeeper - Панель";
        part header : Header;
        part mileageSection : MileageSection;
        part upcomingSection : UpcomingSection;
    }

    part def Header {
        attribute logo = "CarKeeper";
        attribute notifications = "Уведомления: [ListBox]";
    }

    part def MileageSection {
        attribute title = "Ввод пробега";
        attribute carSelect = "Автомобиль: [ComboBox]";
        attribute mileageInput = "Пробег, км: [TextBox]";
        part saveBtn : SaveMileageButton;
    }

    part def UpcomingSection {
        attribute title = "Предстоящие работы";
        attribute counters = "Просрочено: 2 | Скоро: 3";
        attribute table = "Работа | Срок | Статус";
        part addRecordBtn : AddRecordButton;
    }

    part def SaveMileageButton {
        attribute label = "Сохранить";
    }
    part def AddRecordButton {
        attribute label = "+ Запись";
    }
}

package CarKeeper_Plan {
    part def PlanPage {
        attribute title = "План ТО";
        part carInfo : CarInfo;
        part planTable : PlanTable;
        part addItemBtn : AddItemButton;
    }

    part def CarInfo {
        attribute car = "Skoda Octavia 1.6 MPI";
        attribute mileage = "Пробег: 56 000 км";
    }

    part def PlanTable {
        attribute table = "Работа | Интервал | Срок | Статус";
        attribute statusFilter = "Статус: [ComboBox]";
    }

    part def AddItemButton {
        attribute label = "+ Добавить работу";
    }
}

package CarKeeper_Record {
    part def RecordPage {
        attribute title = "Новая запись журнала";
        part mainInputs : MainInputs;
        part planItems : PlanItems;
        part partsSection : PartsSection;
    }

    part def MainInputs {
        attribute dateInput = "Дата: [DatePicker]";
        attribute mileageInput = "Пробег, км: [TextBox]";
        attribute placeInput = "Где выполнено: [TextBox]";
    }

    part def PlanItems {
        attribute title = "Выполненные работы";
        attribute items = "Позиции плана: [CheckBox]";
    }

    part def PartsSection {
        attribute table = "Расходник | Артикул | Цена";
        attribute workCost = "Стоимость работ: [TextBox]";
        part saveBtn : SaveButton;
    }

    part def SaveButton { attribute label = "Сохранить"; }
}

package CarKeeper_Expenses {
    part def ExpensesPage {
        attribute title = "Расходы";
        part periodFilter : PeriodFilter;
        part summary : Summary;
        part chart : Chart;
    }

    part def PeriodFilter {
        attribute carSelect = "Автомобиль: [ComboBox]";
        attribute period = "Период: [DatePicker]";
    }

    part def Summary {
        attribute total = "Итого: 1 284,50 BYN";
        attribute perKm = "1 км: 0,09 BYN";
        part exportBtn : ExportButton;
    }

    part def Chart { attribute byMonth = "[BarChart]"; }
    part def ExportButton {
        attribute label = "Экспорт в PDF";
    }
}

package CarKeeper_Regulations {
    part def RegulationsPage {
        attribute title = "Регламенты ТО";
        part engineTabs : EngineTabs;
        part itemsTable : ItemsTable;
        part saveBtn : SaveButton;
    }

    part def EngineTabs {
        attribute tabs = "Бензин | Дизель";
    }

    part def ItemsTable {
        attribute table = "Работа | Км | Месяцы";
        attribute category = "Категория: [ComboBox]";
    }

    part def SaveButton { attribute label = "Сохранить"; }
}
