
#include <iostream>
#include <unistd.h>
#include <vector>
#include "./generated/python_gym.grpc.pb.h"
#include "./generated/python_gym.pb.h"
#include <string.h>

#include <grpcpp/grpcpp.h>

class grpcGymClient {
public:
    grpcGymClient(std::shared_ptr<grpc::Channel> channel)
            : stub_(pythonGym::pythonGym::NewStub(channel)) {}

    // Assembles the client's payload, sends it and presents the response back
    // from the server.
    pythonGym::DataSet next(const pythonGym::DataSet& x) {
        // Data we are sending to the server.

        // Context for the client. It could be used to convey extra information to
        // the server and/or tweak certain RPC behaviors.
        grpc::ClientContext context;

        pythonGym::DataSet result;
        // The actual RPC.
        grpc::Status status = stub_->next(&context, x, &result);

        // Act upon its status.
        if (status.ok()) {
            return result;
        } else {
            std::cout << status.error_code() << ": " << status.error_message()
                      << std::endl;
            return result;
        }
    }

private:
    std::unique_ptr<pythonGym::pythonGym::Stub> stub_;
};

struct compareDataLabel
{
    const char * m_label;
    compareDataLabel(const char* label): m_label(label) {}

    bool operator()(const pythonGym::Data &data) {
        return strcmp(m_label, data.id().c_str()) == 0;
    }
};

void compute_grpcInterface(double x[], int size_x, const char* in_label[], int size_in_label, const char* out_label[], int size_out_label, double y[], int size_y) {
    static auto channel = grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials());
    static grpcGymClient client(channel);

    if (size_x != size_in_label){
        std:std::cerr << "Invalid number of input labels ! ( expected ="<<  size_x <<", got = " << size_in_label << ")" << std::endl;
        return;
    }

    if (size_y != size_out_label){
        std::cerr << "Invalid number of output labels ! ( expected ="<<  size_y <<", got = " << size_out_label << ")" << std::endl;
        return;
    }

    // Process input data !
    pythonGym::DataSet input_data;
    for(int i=0; i<size_x; i++) {
        pythonGym::Data * batch_data = input_data.add_data();
        batch_data->set_id(in_label[i]);
        batch_data->set_value(x[i]);
    }

    // Send and wait data
    pythonGym::DataSet output_data = client.next(input_data);

    // Process output data !
    if ( output_data.data_size() != size_y) {
        std::cerr << "Received more data than expected ! (receive "<< output_data.data_size()  << " reals, expected "<< size_y <<" reals)"<< std::endl;
    }

    for(int i=0; i<size_y; i++) {
        auto it = std::find_if(output_data.data().cbegin(), output_data.data().cend(), compareDataLabel(out_label[i]));

        if (it == output_data.data().cend()) {
            std::cerr << "Can't find the value " <<  out_label[i] << " in the receive data ! "<< std::endl;
            return;
        }

        y[i] = it->value();
    }

}



extern "C" {// why I'm using this C style proxy  => https://www.ibm.com/docs/en/i/7.1?topic=linkage-name-mangling-c-only
void grpcInterface(double x[], int size_x, const char* in_label[], int size_in_label, const char* out_label[], int size_out_label, double y[], int size_y){
    compute_grpcInterface(x, size_x, in_label, size_in_label, out_label, size_out_label, y, size_y);
    }
}