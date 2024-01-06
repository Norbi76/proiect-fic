module register_file  
 (  
      input                    clk,  
      input                    rst,  
      // write port  
      input                    reg_write_en,  
      input          [2:0]     reg_write_dest,  
      input          [15:0]     reg_write_data,  
      //read port 1  
      input          [2:0]     reg_read_addr_1,  
      output          [15:0]     reg_read_data_1,  
      //read port 2  
      input          [2:0]     reg_read_addr_2,  
      output          [15:0]     reg_read_data_2,
      output  [15:0] reg0,
      output  [15:0] reg1,
      output  [15:0] reg2,
      output  [15:0] reg3,
      output  [15:0] reg4,
      output  [15:0] reg5,
      output  [15:0] reg6,  
      output  [15:0] reg7  
 );  
      reg     [15:0]     reg_array [7:0];  
      // write port  
      //reg [2:0] i;  
      always @ (posedge clk or posedge rst) begin  
           if(rst) begin  
                reg_array[0] <= 16'b0;  
                reg_array[1] <= 16'b0;  
                reg_array[2] <= 16'b0;  
                reg_array[3] <= 16'b0;  
                reg_array[4] <= 16'b0;  
                reg_array[5] <= 16'b0;  
                reg_array[6] <= 16'b0;  
                reg_array[7] <= 16'b0;       
           end  
           else begin  
                if(reg_write_en) begin  
                     reg_array[reg_write_dest] <= reg_write_data;  
                end  
           end  
      end  
      assign reg_read_data_1 = ( reg_read_addr_1 == 0)? 16'b0 : reg_array[reg_read_addr_1];  
      assign reg_read_data_2 = ( reg_read_addr_2 == 0)? 16'b0 : reg_array[reg_read_addr_2];  
      

      assign reg0 = reg_array[0];
      assign reg1 = reg_array[1];
      assign reg2 = reg_array[2];
      assign reg3 = reg_array[3];
      assign reg4 = reg_array[4];
      assign reg5 = reg_array[5];
      assign reg5 = reg_array[5];
      assign reg6 = reg_array[6];
      assign reg7 = reg_array[7];
 endmodule