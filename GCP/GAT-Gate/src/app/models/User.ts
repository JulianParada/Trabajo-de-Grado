export class User{
  public NOMBRE: string;
  public PASSWORD: string;
  public EMAIL: string;
  public ESTADO: string;
  public ROL: string;

  constructor(nombre: string, email: string, estado: string, rol: string){
    this.NOMBRE = nombre;
    this.PASSWORD = '';
    this.EMAIL = email;
    this.ESTADO = estado;
    this.ROL = rol;
  }

}
