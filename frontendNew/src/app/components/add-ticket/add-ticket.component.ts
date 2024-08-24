import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-add-ticket',
  templateUrl: './add-ticket.component.html',
  styleUrls: ['./add-ticket.component.css']
})
export class AddTicketComponent {

  form!: FormGroup;

  constructor(private ticketService: MainService, private formg: FormBuilder) { 
    this.form = this.formg.group({
      files: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.msg_error = '';
    this.msg_success = '';
  }

  selectedFiles: File[] = [];

  msg_error: string = '';
  msg_success: string = '';


  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files) {
      this.selectedFiles = Array.from(input.files); // Recoge los archivos seleccionados
    }
  }

  OnSubmit(): void {
    this.msg_error = '';
    this.msg_success = '';
    if (this.form.valid){
      if (this.selectedFiles.length > 0) {

        const formData = new FormData();
        this.selectedFiles.forEach(file => formData.append('files', file));
        
        // Aquí se enviaría el formulario al servidor
        this.ticketService.add_ticket(formData).subscribe((data: any) => {
          console.log(data);
          this.msg_success = data.message;
        }, (error: any) => {
          console.log(error);
          this.msg_error = error.error.message;});
      }
      else {
        this.msg_error = 'No se ha seleccionado ningún archivo';
      }
    }
  }
}
