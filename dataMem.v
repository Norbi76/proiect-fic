module data_memory  
 (  
      input                         clk,  
      
      input     [15:0]               mem_access_addr,  // address input, shared by read and write port  
     
      input     [15:0]               mem_write_data,     // write port
      input                         mem_write_en,  
      
      input mem_read,        // read port
  
      output     [15:0]               mem_read_data  
 );  
      integer i;  
      reg [15:0] ram [255:0];  
      wire [7 : 0] ram_addr = mem_access_addr[8 : 1];  
      initial begin  
        //    for(i=0;i<256;i=i+1)  
        //         ram[i] <= 16'd0;
                ram[0]  = 16'b0000000000000011;
                ram[1]  = 16'b0000000000000110;
                ram[2]  = 16'b0;
                ram[3]  = 16'b0;
                ram[4]  = 16'b0;
                ram[5]  = 16'b0;
                ram[6]  = 16'b0;
                ram[7]  = 16'b0;
                ram[8]  = 16'b0;
                ram[9]  = 16'b0;
                ram[10] = 16'b0;
                ram[11] = 16'b0;
                ram[12] = 16'b0;
                ram[13] = 16'b0;
                ram[14] = 16'b0;
                ram[15] = 16'b0;

      end  
      always @(posedge clk) begin  
           if (mem_write_en)  
                ram[ram_addr] <= mem_write_data;  
      end  
      assign mem_read_data = (mem_read==1'b1) ? ram[ram_addr]: 16'd0;   
 endmodule