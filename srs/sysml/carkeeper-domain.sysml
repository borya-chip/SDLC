package CarKeeperDomain {
    // Модель предметной области CarKeeper (приложение В спецификации).
    // Композиция («владеет») записана как part, ссылки — как ref.
    // Версия 0.2: добавлены TyreSet, CarDocument, RecordPart.

    private import ScalarValues::*;

    enum def Role { owner; admin; }
    enum def EngineType { petrol; diesel; hybrid; electric; }
    enum def Status { ok; soon; overdue; }
    enum def Season { summer; winter; allSeason; }

    part def User {
        attribute email : String;
        attribute passwordHash : String;
        attribute role : Role;
        attribute remindByEmail : Boolean;
        attribute warnKm : Integer;
        attribute warnDays : Integer;
        part cars : Car[0..*];
    }

    part def Car {
        attribute make : String;
        attribute model : String;
        attribute year : Integer;
        attribute engineType : EngineType;
        attribute vin : String;
        attribute annualMileage : Integer;
        attribute archived : Boolean;
        part readings : MileageReading[0..*];
        part plan : PlanItem[1..*];
        part records : ServiceRecord[0..*];
        part tyres : TyreSet[0..*];
        part documents : CarDocument[0..*];
    }

    part def MileageReading {
        attribute date : String;
        attribute mileage : Integer;
    }

    part def Regulation {
        attribute name : String;
        attribute engineType : EngineType;
        part items : RegulationItem[1..*];
    }

    part def RegulationItem {
        attribute title : String;
        attribute category : String;
        attribute intervalKm : Integer;
        attribute intervalMonths : Integer;
    }

    part def PlanItem {
        attribute title : String;
        attribute intervalKm : Integer;
        attribute intervalMonths : Integer;
        attribute lastDate : String;
        attribute lastMileage : Integer;
        attribute enabled : Boolean;
        ref source : RegulationItem[0..1];
        part notifications : Notification[0..*];
    }

    part def ServiceRecord {
        attribute date : String;
        attribute mileage : Integer;
        attribute place : String;
        attribute labourCost : Real;
        attribute total : Real;
        part parts : RecordPart[0..*];
        part attachments : Attachment[0..5];
        ref closes : PlanItem[0..*];
    }

    part def RecordPart {
        attribute name : String;
        attribute manufacturer : String;
        attribute partNumber : String;
        attribute quantity : Integer;
        attribute price : Real;
    }

    part def Attachment {
        attribute fileName : String;
        attribute contentType : String;
        attribute size : Integer;
    }

    part def Notification {
        attribute status : Status;
        attribute createdAt : String;
        attribute read : Boolean;
    }

    part def TyreSet {
        attribute season : Season;
        attribute brand : String;
        attribute mileage : Integer;
        attribute installed : Boolean;
    }

    part def CarDocument {
        attribute type : String;
        attribute expiresAt : String;
    }
}
