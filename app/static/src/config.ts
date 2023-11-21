import {
  ICharterer,
  IWaterarea,
  IShip,
  ICertType,
  ICertificate,
  IMariner,
} from "./types";

export const STATIC_URL = "/static/src/assets/";

export const defaultMariner: IMariner = {
  pk: "",
  name: "",
  shipPk: "",
  birthday: "",
  duty: "",
  registerDate: "",
  isRetired: false,
  retiredDate: "",
  job: "",
  dailyFee: 0,
  platoon: "",
  prevAffilication: "",
  code: "",
  mobilePhone: "",
  homePhone: "",
  graduate: "",
  graduateDate: "",
  qualGrade: "",
  boardedYears: 0,
  note: "",
  placeBorn: "",
  placeResidence: "",
  photoUris: "",
};

export const defaultCertificate: ICertificate = {
  pk: "",
  certtypePk: "",
  shipPk: "",
  marinerPk: "",
  kind: 1,
  issuePutinDate: "",
  issueDepartment: "",
  issueId: "",
  issueDate: "",
  issueExpireDate: "",
  issueAccount: "",
  issuePrice: 0,
  issueRegfee: 0,
  issueAmount: 0,
};

export const defaultCerttype : ICertType = {
  pk: "",
  name: "",
  agency: "",
  note: "",
  kind: 1,
}

export const defaultShip: IShip = {
  pk: "",
  name: "",
  registerdDate: "",
  isRemoved: false,
  removedDate: "",
  shipType: "",
  buildYear: 0,
  flag: "",
  homeport: "",
  grossTonnage: 0,
  deadWeight: 0,
  length: 0,
  beam: 0,
  depth: 0,
  draught: 0,
  note: "",
  photoUris: "",
  regNumber: "",
  callsign: "",
  imoNumber: "",
};
