`timescale 1ns / 1ps
//fpga4student.com: FPGA projects, Verilog projects, VHDL projects
// Verilog project: Verilog code for 16-bit MIPS Processor
// Testbench Verilog code for 16 bit single cycle MIPS CPU  
 module tb_mips16;  
      // Inputs  
      reg clk;  
      reg reset;  
      // Outputs  
      wire [15:0] pc_out;  
      wire [15:0] alu_result, reg0, reg1, reg2, reg3, reg4, reg5, reg6, reg7, instruction;  
      // Instantiate the Unit Under Test (UUT)  
      mips_16 uut (  
           .clk(clk),   
           .reset(reset),   
           .pc_out(pc_out),   
           .alu_result(alu_result),
           .reg0(reg0),  
           .reg1(reg1),  
           .reg2(reg2),  
           .reg3(reg3),  
           .reg4(reg4),  
           .reg5(reg5),  
           .reg6(reg6),  
           .reg7(reg7),
           .instr_test(instruction) 
      );  
      initial begin  
           clk = 0;  
           forever #10 clk = ~clk;  
      end  
      initial begin  
           // Initialize Inputs  
        $monitor ("register 0=%d, register 1=%d, register 2=%d, register 3=%d, register 4=%d, register 5=%d, register 6=%d, register 7=%d, instruction = %b",
         reg0, reg1, reg2, reg3, reg4, reg5, reg6, reg7, instruction);
        // $monitor ("current instruction = %d", instruction);  
        reset = 1;  
           // Wait 100 ns for global reset to finish  
        #100;  
        reset = 0;

        if(reg1 != 0)
          #100;
          reset = 1;
            
        // Add stimulus here  
      end  
 endmodule  