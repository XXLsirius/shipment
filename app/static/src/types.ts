export interface ICertType {
  pk: string;
  name: string;
  agency: string;
  note: string;
  kind: number;
}
export interface IMariner {
  pk: string;
  name: string;
  shipPk: string;
  birthday: string;
  duty: string;
  registerDate: string;
  isRetired: boolean;
  retiredDate: string;
  job: string;
  dailyFee: number;
  platoon: string;
  prevAffilication: string;
  code: string;
  mobilePhone: string;
  homePhone: string;
  graduate: string;
  graduateDate: string;
  qualGrade: string;
  boardedYears: number;
  note: string;
  placeBorn: string;
  placeResidence: string;
  photoUris: string;
}

export interface IShip {
  pk: string;
  name: string;
  registerdDate: string;
  isRemoved: false;
  removedDate: string;
  shipType: string;
  buildYear: number;
  flag: string;
  homeport: string;
  grossTonnage: number;
  deadWeight: number;
  length: number;
  beam: number;
  depth: number;
  draught: number;
  note: string;
  photoUris: string;
  regNumber: string;
  callsign: string;
  imoNumber: string;
}


export interface ICertificate {
  pk: string;
  certtypePk: string;
  shipPk: string;
  marinerPk: string;
  kind: number;
  issuePutinDate: string;
  issueDepartment: string;
  issueId: string;
  issueDate: string;
  issueExpireDate: string;
  issueAccount: string;
  issuePrice: number;
  issueRegfee: number;
  issueAmount: number;
  certtype? : ICertType

}

export interface ICharterer {
  pk: string;
  company: string;
  nation: string;
  phone: string;
  email: string;
  note: string;
}

export interface IWaterarea {
  pk: string;
  name: string;
  note: string;
}

export type FnLoadCallback<T> = (data: T[], total_count?: number) => void;

export type FnLoad<T> = (
  page: number,
  size: number,
  searchQuery: any,
  callback: FnLoadCallback<T>
) => void;

export type FnDelete<T> = (item: T, callback: (res: any) => void) => void;

function getQLType(value: any): string {
  let type = typeof value;
  switch (type) {
    case "string":
      return "String";
    case "number":
      return "Int";
    case "boolean":
      return "Boolean";
    default:
      return "String";
  }
}

export function getUpdateQLData(obj: any): string {
  let keys = Object.keys(obj);
  return keys.map((key) => `${key}: $${key}`).join(" ");
}

export function getUpdateQLParams(obj: any): string {
  let keys = Object.keys(obj);
  return keys.map((key) => `$${key}: ${getQLType(obj[key])}!`).join(" ");
}

export function getQueryReturn(obj: any) : string {
  let keys = Object.keys(obj);

  const _ =keys.map((key) => `${key}`).join(" "); 
  console.log('getQueryReturn ', _);
  return _;
}