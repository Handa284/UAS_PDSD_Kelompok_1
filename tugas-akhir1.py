import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu

# Load data
@st.cache_data
def load_data():
    df_data_customer = pd.read_csv('customers_dataset.csv')
    df_data_geolocation = pd.read_csv('geolocation_dataset.csv')
    df_data_order_item = pd.read_csv('order_items_dataset.csv')
    df_data_payment = pd.read_csv('order_payments_dataset.csv')
    df_data_order = pd.read_csv('orders_dataset.csv')
    df_data_product_category = pd.read_csv('product_category_name_translation.csv')
    df_data_product = pd.read_csv('products_dataset.csv')

    return df_data_customer, df_data_geolocation, df_data_order_item, df_data_payment, df_data_order, df_data_product_category, df_data_product
df_data_customer, df_data_geolocation, df_data_order_item, df_data_payment, df_data_order, df_data_product_category, df_data_product = load_data()

def Analisis_Perkembangan () :
    df_data_order.dropna(subset=['order_approved_at','order_delivered_carrier_date','order_delivered_customer_date'], axis=0, inplace=True)
    df_data_order.reset_index(drop=True, inplace=True)

    df_data_product.dropna(subset=['product_category_name','product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm'], axis=0, inplace=True)
    df_data_product.reset_index(drop=True, inplace=True)

    data_payment = pd.merge(df_data_payment, df_data_order, on='order_id', how='inner')
    data_payment = data_payment.loc[:, ['order_purchase_timestamp', 'payment_value']]
    if data_payment['order_purchase_timestamp'].dtypes != 'datetime64[ns]':
        data_payment['order_purchase_timestamp'] = pd.to_datetime(data_payment['order_purchase_timestamp'], errors='coerce')

    data_payment['order_purchase_timestamp'] = data_payment['order_purchase_timestamp'].dt.date

    data_payment['year_month'] = pd.to_datetime(data_payment['order_purchase_timestamp']).dt.to_period('M')
    data_payment = data_payment.groupby('year_month')['payment_value'].sum()
    data_payment = pd.DataFrame(data_payment)


    st.header("Tabel Perkembangan Total Pendapatan")
    st.dataframe(data_payment)
    # Streamlit app
    st.header('Grafik Pertumbuhan Total Pendapatan')

    # Create a figure and plot on it
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(data_payment.index.astype(str), data_payment['payment_value'], marker='o')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Pertumbuhan (%)')
    ax.set_title('Grafik Pertumbuhan Total Pendapatan')

    # Set x-axis ticks and labels to show every 3rd month
    x_ticks = data_payment.index.astype(str)[::3]  # Show every 3rd month
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks, rotation=45)  # Rotate the labels for better readability

    # Show the plot using st.pyplot() with the figure object
    st.pyplot(fig)
    
    with st.expander("Penjelasan Total Pendapatan Tiap Bulan") :
        st.write('dilihat dari grafik, pertumbuhan pendapatan semakin meningkat awal awal dan puncaknya berada pada bulan november 2017, setelah itu pendapatan menjadi cukup stabil tetapi turun di bulan terakhir. solusi untuk perusahaan adalah dengan meningkatkan aspek aspek seperti layanan, kualitas produk, dan lainnya agar penjulaan dapat kembali meningkat')
    
    
    
    
    
def Analisis_Kota():
    #Membuat sebuah data yang sudah di satukan dari 3 tabel menggunakan metode merge
    df_data_order.dropna(subset=['order_approved_at','order_delivered_carrier_date','order_delivered_customer_date'], axis=0, inplace=True)
    df_data_order.reset_index(drop=True, inplace=True)
    
    data_customer = pd.merge(df_data_customer, df_data_order, on='customer_id', how='inner')
    data_customer = pd.merge(data_customer, df_data_order_item, on='order_id', how='inner')

    data_customer['price'] = data_customer['price'] * data_customer['order_item_id']
    data_customer = data_customer.loc[:, ['customer_id', 'customer_city', 'price']]

    #Menentukan kota dari tertinggi
    grup = data_customer.groupby(['customer_city'])['price'].sum()
    grup1 = grup.nlargest(5)

    st.header("Tabel Kota dari Tertinggi")
    st.dataframe(grup1)
    
    # Streamlit app
    st.header("Diagram Pie 5 Kota Dengan Penjualan Tertinggi")

    # Plot pie chart
    fig, ax = plt.subplots()
    expose = [0.1, 0, 0, 0, 0]  # Explode the first slice (optional)
    ax.pie(grup1, labels=grup1.index, autopct='%1.1f%%', shadow=True, startangle=50, explode=expose)
    ax.set_title("Top 5 Kota Penjualan dari yang Tertinggi")
    ax.legend(loc="best", bbox_to_anchor=(1.05, 1))

    # Show the plot using st.pyplot() with the figure object
    st.pyplot(fig)

    #Menentukan kota dari terendah
    grup = data_customer.groupby(['customer_city'])['price'].sum()
    grup2 = grup.nsmallest(5)

    st.header("Tabel Kota dari Terendah")
    st.dataframe(grup2)


    # Streamlit app
    st.header("Diagram Pie 5 Kota Dengan Penjualan Terendah")

    # Plot pie chart
    fig, ax = plt.subplots()
    expose = [0.1, 0, 0, 0, 0]  # Explode the first slice (optional)
    ax.pie(grup2, labels=grup2.index, autopct='%1.1f%%', shadow=True, startangle=50, explode=expose)
    ax.set_title("Top 5 Kota Penjualan dari yang Terendah")
    ax.legend(loc="best", bbox_to_anchor=(1.05, 1))

    # Show the plot using st.pyplot() with the figure object
    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Kota") :
        st.write('Kota Sao Paulo memiliki total penjualan yang paling tinggi dan paling signifikan dibandingkan dengan kota-kota lainnya. Sedangkan kota <b>polo petroquimico de triunfo</b> memiliki total penjualan terendah dari kota-kota lainnya.<br> 5 kota dengan penjualan tertinggi tersebut bisa menjadi pusat strategi bisnis dan marketing perusahaan, namun apabila sumber daya yang dimiliki sangat terbatas, kita bisa memusatkannya lagi sehingga hanya 2 kota saja yaitu Sao Paulo dan Rio De Janeiro. Sedangkan untuk 5 kota terendah, ini akan menjadi bahan penelitian bagi perusahaan, mengapa hal demikian bisa terjadi.')
    




def Analisis_Pemesanan():
    df_data_order.dropna(subset=['order_approved_at','order_delivered_carrier_date','order_delivered_customer_date'], axis=0, inplace=True)
    df_data_order.reset_index(drop=True, inplace=True)
    
    data_pemesanan = pd.merge(df_data_payment, df_data_order, on='order_id', how='inner')
    data_pemesanan = data_pemesanan.loc[:, ['order_purchase_timestamp', 'order_id']]
    if data_pemesanan['order_purchase_timestamp'].dtypes != 'datetime64[ns]':
        data_pemesanan['order_purchase_timestamp'] = pd.to_datetime(data_pemesanan['order_purchase_timestamp'], errors='coerce')

    data_pemesanan['order_purchase_timestamp'] = data_pemesanan['order_purchase_timestamp'].dt.date

    data_pemesanan['year_month'] = pd.to_datetime(data_pemesanan['order_purchase_timestamp']).dt.to_period('M')
    data_pemesanan = data_pemesanan.groupby('year_month')['order_id'].count()
    data_pemesanan = pd.DataFrame(data_pemesanan)
    st.header("Tabel Banyaknya Pemesanan Dalam Periode Bulan")
    st.dataframe(data_pemesanan)

    # Streamlit app
    st.header('Grafik Pertumbuhan Total Pemesanan')


    # Plot line chart
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(data_pemesanan.index.astype(str), data_pemesanan.values, marker='o')  # Convert PeriodIndex to string for x-axis
    ax.set_title('Grafik Pertumbuhan Total Pemesanan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Pertumbuhan (%)')

    # Set x-axis ticks and labels
    x_labels = []
    for i, period in enumerate(data_pemesanan.index):
        if i % 2 == 0:  # Show label for every two months
            x_labels.append(period.strftime('%b %Y'))
        else:
            x_labels.append('')  # Empty label for other months
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels)

    # Show the plot using st.pyplot() with the figure object
    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Total Pemesanan") :
        st.write('Pertumbuhan pemesanan meningkat cukup signifikan pada awal-awal hingga puncaknya pada november tahun 2017, tetapi dalam 9 bulan terakhir tidak ada peningkatan yang lebih tinggi daripada peningkatan pada november tahun 2017. Jika hal ini tidak segera diatasi maka ada kemungkinan trend akan mengalami penurunan. Berikut solusi yang dapat dipertimbangkan untuk masalah ini  yaitu membuat promosi musiman dan melakukan program loyalitas pelanggan.')
    
    

def Analisis_Penjualan() :
    data_product = pd.merge(df_data_order_item, df_data_product, on='product_id', how='inner')
    data_product = pd.merge(data_product, df_data_product_category, on='product_category_name', how='inner')
    # Memilih kolom yang diperlukan

    data_product = data_product.loc[:, ['product_id', 'product_category_name','product_category_name_english']]
    # Menghitung jumlah penjualan setiap produk
    product_counts = data_product['product_category_name_english'].value_counts()

    # Menampilkan 5 produk dengan penjualan terbanyak
    top_5_products = product_counts.nlargest(5)
    st.header("Tabel 5 Produk Dengan Penjualan Terbanyak")
    st.dataframe(top_5_products)

    # Streamlit app
    st.header('Diagram Pie 5 Produk Paling Banyak Diminati')

    # Plot pie chart
    fig, ax = plt.subplots()
    expose = [0.1, 0, 0, 0, 0]  # Explode the first slice (optional)
    ax.pie(top_5_products, labels=top_5_products.index, autopct='%1.1f%%', shadow=True, explode=expose)
    ax.set_title('5 Produk Paling Banyak Diminati')
    ax.legend(loc="best", bbox_to_anchor=(1.8, 1))

    # Show the plot using st.pyplot() with the figure object
    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Penjualan") :
        st.write('Product bed_beth_table menjadi menjadi salah satu kategori yang paling diminati dibandingkan product lainnya sehingga perusahaan dapat mengaturstrategi marketing dari hasil data yang didapatkan')
    
    
def Analisis_Pembayaran(df_data_payment) :
    df_data_payment = df_data_payment.loc[:, ['order_id', 'payment_type']]
    # Menghitung jenis pembayaran yang digunakan
    payment_counts = df_data_payment['payment_type'].value_counts()

    # Menampilkan 4 jenis pembayaran terbanyak
    top_payments = payment_counts.nlargest(4)
    st.header("Tabel Dengan 4 Jenis Pembayaran Terbanyak")
    st.dataframe(top_payments)

    # Streamlit app
    st.header('Diagram Pie 4 Jenis Pembayaran Terbanyak digunakan')

    # Plot pie chart
    fig, ax = plt.subplots()
    ax.pie(top_payments, labels=top_payments.index, autopct='%1.1f%%', shadow=True)
    ax.set_title('4 Jenis Pembayaran Terbanyak digunakan')
    ax.legend(loc="best", bbox_to_anchor=(1.5, 1))

    # Show the plot using st.pyplot() with the figure object
    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Jenis Pembayaran") :
        st.write('Credit card merupakan metode pembayaran yang paling sering digunakan. jika perusahaan ingin meningkatkan pendapatan, perusahaan dapat melakukan promosi atau diskon khusus untuk penggunaan metode pembayaran tertentu. Misalnya, diskon 10% untuk pembayaran dengan voucher. selain memberikan voucher perusahaan dapat meLakukan edukasi kepada pelanggan mengenai keuntungan menggunakan metode pembayaran lainnya. Misalnya, pembayaran dengan boleto bisa lebih aman karena tidak memerlukan detail kartu kredit.')
    
    

with st.sidebar :
    selected = option_menu('Menu',['Analisis Total Pendapatan','Analisis Kota','Analisis Total Pemesanan','Analisis Penjualan','Analisis Jenis Pembayaran'],
    icons =["graph-up", "graph-up", "graph-up", "graph-up", "graph-up"],
    menu_icon="cast",
    default_index=0)
    
if (selected == 'Analisis Total Pendapatan') :
    st.title(f"Analisis Total Pendapatan")
    Analisis_Perkembangan()
elif (selected == 'Analisis Kota') :
    st.title(f"Analisis Kota Penjualan Tertinggi dan Terendah")
    Analisis_Kota()
elif (selected == 'Analisis Total Pemesanan') :
    st.title(f"Analisis Total Pemesanan")
    Analisis_Pemesanan()
elif (selected == 'Analisis Penjualan') :
    Analisis_Penjualan()
elif (selected == 'Analisis Jenis Pembayaran') :
    Analisis_Pembayaran(df_data_payment)
    